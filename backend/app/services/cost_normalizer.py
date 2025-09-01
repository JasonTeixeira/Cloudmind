"""
Cost normalization, unit economics, and tag hygiene auditing services.
Lightweight MVP that can be swapped with real data sources later.
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from uuid import UUID
import datetime as dt
import logging

from app.core.config import settings


logger = logging.getLogger(__name__)


class CostNormalizer:
    """Normalizes raw cloud billing events into a unified shape (MVP)."""

    def __init__(self) -> None:
        pass

    def normalize_events(self, raw_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return normalized events with common fields.
        This MVP simply passes through with a stable key set.
        """
        normalized: List[Dict[str, Any]] = []
        for e in raw_events:
            normalized.append({
                "provider": e.get("provider", "unknown"),
                "project_id": e.get("project_id"),
                "account": e.get("account"),
                "service": e.get("service"),
                "region": e.get("region"),
                "usage_amount": float(e.get("usage_amount", 0.0)),
                "cost": float(e.get("cost", 0.0)),
                "currency": e.get("currency", "USD"),
                "timestamp": e.get("timestamp") or dt.datetime.utcnow().isoformat(),
                "tags": e.get("tags", {}),
            })
        return normalized

    def compute_unit_economics(
        self,
        user_id: str | UUID,
        project_id: Optional[UUID] = None,
        group_by: str = "project",
    ) -> Dict[str, Any]:
        """Compute basic unit economics summary (MVP/demo data)."""
        now = dt.datetime.utcnow().isoformat()
        # Return placeholder values; wire to real storage later
        return {
            "generated_at": now,
            "group_by": group_by,
            "project_id": str(project_id) if project_id else None,
            "currency": "USD",
            "period": "last_30d",
            "totals": {
                "cost_total": 12345.67,
                "usage_total": 98765.43,
                "avg_cost_per_unit": 0.125,
            },
            "breakdown": [
                {"key": "service:compute", "cost": 4500.0, "usage": 32000.0},
                {"key": "service:storage", "cost": 3800.0, "usage": 52000.0},
                {"key": "service:network", "cost": 3045.67, "usage": 14765.43},
            ],
        }


class TagHygieneAuditor:
    """Detects tag/label hygiene issues and proposes fixes (MVP)."""

    REQUIRED_TAGS = ["owner", "environment", "application"]

    def audit(self, sample_resources: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Return a simple audit report with missing/invalid tags.
        This MVP returns a static report to exercise the endpoint.
        """
        issues = [
            {
                "resource_id": "aws:ec2:i-012345",
                "missing": ["owner"],
                "invalid": {"environment": "prod-1 (should be prod|staging|dev)"},
                "suggested_fix": {"owner": "team-xyz", "environment": "prod"},
            },
            {
                "resource_id": "gcp:compute:instance-42",
                "missing": ["application"],
                "invalid": {},
                "suggested_fix": {"application": "web-api"},
            },
        ]
        return {
            "required_tags": self.REQUIRED_TAGS,
            "total_resources_scanned": 2,
            "issues_found": len(issues),
            "issues": issues,
        }


class SlackDigestService:
    """Sends daily cost digests to Slack/Teams (stub)."""

    def send_daily_digest(self) -> Dict[str, Any]:
        if not settings.ENABLE_SLACK_DIGESTS:
            return {"sent": False, "reason": "digests_disabled"}
        webhook = getattr(settings, "SLACK_WEBHOOK_URL", None)
        summary = {
            "title": "Daily Cost Digest",
            "text": "Total cost: $12,345.67 (MVP stub)\nTop services: compute, storage, network",
        }
        # If no webhook configured, log only
        if not webhook:
            logger.info("Daily cost digest (log only): %s", summary)
            return {"sent": False, "reason": "no_webhook_configured", "preview": summary}
        try:
            import json, urllib.request  # stdlib only
            req = urllib.request.Request(
                webhook,
                data=json.dumps({"text": f"*{summary['title']}*\n{summary['text']}"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                ok = 200 <= resp.getcode() < 300
            return {"sent": ok}
        except Exception as e:
            logger.warning("Slack digest post failed: %s", e)
            return {"sent": False, "error": str(e)}


