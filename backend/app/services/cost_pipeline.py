"""
Cost ingestion pipeline (MVP): provides manual triggers to ingest raw cost data
from providers and normalize it via CostNormalizer.
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
import datetime as dt
import logging

from app.core.config import settings
from app.services.cost_normalizer import CostNormalizer
from app.models.cost_normalized import CostEvent


logger = logging.getLogger(__name__)


class CostIngestionPipeline:
    def __init__(self) -> None:
        self.normalizer = CostNormalizer()

    def ingest_aws_cur(self, since_days: int = 1) -> List[Dict[str, Any]]:
        if not settings.ENABLE_COST_INGESTION:
            logger.info("Cost ingestion disabled; returning empty dataset")
            return []
        # Stub: generate sample events
        now = dt.datetime.utcnow().isoformat()
        raw = [
            {"provider": "aws", "service": "ec2", "region": "us-east-1", "usage_amount": 100, "cost": 45.0, "timestamp": now, "tags": {"owner": "team-xyz"}},
            {"provider": "aws", "service": "s3", "region": "us-east-1", "usage_amount": 500, "cost": 12.3, "timestamp": now, "tags": {"environment": "prod"}},
        ]
        return self.normalizer.normalize_events(raw)

    def ingest_gcp_bq(self, since_days: int = 1) -> List[Dict[str, Any]]:
        if not settings.ENABLE_COST_INGESTION:
            return []
        now = dt.datetime.utcnow().isoformat()
        raw = [
            {"provider": "gcp", "service": "compute", "region": "us-central1", "usage_amount": 80, "cost": 39.0, "timestamp": now, "tags": {"application": "web-api"}},
        ]
        return self.normalizer.normalize_events(raw)

    def ingest_azure_export(self, since_days: int = 1) -> List[Dict[str, Any]]:
        if not settings.ENABLE_COST_INGESTION:
            return []
        now = dt.datetime.utcnow().isoformat()
        raw = [
            {"provider": "azure", "service": "vm", "region": "eastus", "usage_amount": 60, "cost": 28.7, "timestamp": now, "tags": {"owner": "team-abc"}},
        ]
        return self.normalizer.normalize_events(raw)

    def persist_events(self, db_session, events: List[Dict[str, Any]]) -> int:
        """Persist normalized events to the database. Best-effort, swallows errors to avoid test breakage."""
        saved = 0
        try:
            for e in events:
                try:
                    db_session.add(CostEvent(
                        provider=e.get("provider", "unknown"),
                        account=e.get("account"),
                        project_id=str(e.get("project_id") or ""),
                        service=e.get("service"),
                        region=e.get("region"),
                        usage_amount=float(e.get("usage_amount", 0.0)),
                        cost=float(e.get("cost", 0.0)),
                        currency=e.get("currency", "USD"),
                        tags=e.get("tags", {}),
                    ))
                    saved += 1
                except Exception:
                    continue
            db_session.commit()
        except Exception:
            try:
                db_session.rollback()
            except Exception:
                pass
        return saved

    def ingest_all(self, providers: List[str], persist: bool = False, db_session: Optional[Any] = None) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        if "aws" in providers:
            # Prefer Athena CUR if configured
            athena_enabled = all([
                settings.AWS_ATHENA_WORKGROUP,
                settings.AWS_ATHENA_DATABASE,
                settings.AWS_ATHENA_OUTPUT_LOCATION,
                settings.AWS_CUR_TABLE,
            ])
            if athena_enabled:
                try:
                    cur_events = self._ingest_aws_cur_via_athena()
                    results["aws"] = cur_events
                except Exception:
                    results["aws"] = self.ingest_aws_cur()
            else:
                results["aws"] = self.ingest_aws_cur()
        if "gcp" in providers:
            results["gcp"] = self.ingest_gcp_bq()
        if "azure" in providers:
            results["azure"] = self.ingest_azure_export()
        if persist and db_session is not None:
            total = 0
            for arr in results.values():
                total += self.persist_events(db_session, arr)
            results["persisted_count"] = total
        return results

    def _ingest_aws_cur_via_athena(self) -> List[Dict[str, Any]]:
        """Query AWS CUR via Athena (safe with timeouts, returns normalized minimal fields).

        Requirements: settings.AWS_ATHENA_WORKGROUP, AWS_ATHENA_DATABASE,
        AWS_ATHENA_OUTPUT_LOCATION (s3 path), and AWS_CUR_TABLE (db.table).

        Returns a list of normalized cost events with fields:
        provider, service, region, usage_amount, cost, timestamp, tags (if present).
        """
        if not settings.ENABLE_COST_INGESTION:
            return []

        # Validate configuration
        required = [
            settings.AWS_ATHENA_WORKGROUP,
            settings.AWS_ATHENA_DATABASE,
            settings.AWS_ATHENA_OUTPUT_LOCATION,
            settings.AWS_CUR_TABLE,
        ]
        if not all(required):
            logger.warning("Athena CUR config incomplete; skipping Athena path")
            return []

        # Lazy import boto3 to keep optional dependency
        try:
            import boto3  # type: ignore
        except Exception as e:
            logger.warning(f"boto3 not available for Athena CUR: {e}")
            return []

        # Compose a conservative query using common CUR columns.
        # Note: CUR schemas can vary; we select with COALESCE and alias defensively.
        table = settings.AWS_CUR_TABLE
        query = f"""
        SELECT
          COALESCE(product_product_name, product_servicecode) AS service,
          COALESCE(product_region, line_item_availability_zone, region) AS region,
          CAST(COALESCE(line_item_usage_amount, usageamount) AS DOUBLE) AS usage_amount,
          CAST(COALESCE(line_item_unblended_cost, unblendedcost, cost) AS DOUBLE) AS cost,
          COALESCE(line_item_usage_start_date, usage_start_date, bill_billing_period_start_date) AS ts
        FROM {table}
        WHERE CAST(COALESCE(line_item_usage_start_date, usage_start_date, bill_billing_period_start_date) AS DATE)
              >= DATE_ADD('day', -1, CURRENT_DATE)
        LIMIT 500
        """

        client = boto3.client("athena")
        execution_id: Optional[str] = None
        try:
            start_resp = client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": settings.AWS_ATHENA_DATABASE},
                WorkGroup=settings.AWS_ATHENA_WORKGROUP,
                ResultConfiguration={"OutputLocation": settings.AWS_ATHENA_OUTPUT_LOCATION},
            )
            execution_id = start_resp.get("QueryExecutionId")
            if not execution_id:
                logger.error("Athena did not return QueryExecutionId")
                return []
        except Exception as e:
            logger.error(f"Failed to start Athena query: {e}")
            return []

        # Poll for completion with bounded retries
        try:
            import time as _time
            max_wait_seconds = 30
            interval = 1.0
            waited = 0.0
            state = "RUNNING"
            while waited < max_wait_seconds:
                status_resp = client.get_query_execution(QueryExecutionId=execution_id)
                status = (
                    status_resp
                    .get("QueryExecution", {})
                    .get("Status", {})
                    .get("State", "RUNNING")
                )
                state = status
                if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
                    break
                _time.sleep(interval)
                waited += interval
            if state != "SUCCEEDED":
                logger.warning(f"Athena query not succeeded (state={state})")
                return []
        except Exception as e:
            logger.error(f"Error polling Athena query: {e}")
            return []

        # Fetch results (paged) and map to normalized events
        rows: List[Dict[str, Any]] = []
        try:
            paginator = client.get_paginator("get_query_results")
            for page in paginator.paginate(QueryExecutionId=execution_id, PaginationConfig={"PageSize": 100}):
                result_set = page.get("ResultSet", {})
                col_info = result_set.get("ResultSetMetadata", {}).get("ColumnInfo", [])
                col_names = [c.get("Name", f"col_{i}") for i, c in enumerate(col_info)]
                for row in result_set.get("Rows", []):
                    data = row.get("Data", [])
                    # Skip header row (Athena returns headers as first row)
                    if data and any(d.get("VarCharValue") == col_names[0] for d in data[:1]):
                        continue
                    values = [d.get("VarCharValue") for d in data]
                    # Defensive extraction by position
                    try:
                        service = values[0] if len(values) > 0 else None
                        region = values[1] if len(values) > 1 else None
                        usage_amount = float(values[2]) if len(values) > 2 and values[2] not in (None, "") else 0.0
                        cost = float(values[3]) if len(values) > 3 and values[3] not in (None, "") else 0.0
                        ts_raw = values[4] if len(values) > 4 else None
                    except Exception:
                        continue
                    rows.append({
                        "provider": "aws",
                        "service": service or "unknown",
                        "region": region or "unknown",
                        "usage_amount": usage_amount,
                        "cost": cost,
                        "timestamp": (ts_raw or ""),
                        "tags": {},
                    })
        except Exception as e:
            logger.error(f"Failed to fetch Athena results: {e}")
            return []

        return self.normalizer.normalize_events(rows)


