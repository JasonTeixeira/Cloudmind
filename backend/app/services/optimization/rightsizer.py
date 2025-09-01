"""
Rightsizing recommender (MVP): suggests CPU/memory/storage/db downsizing based on
simple thresholds (placeholder data), with dry-run friendly outputs.
"""

from __future__ import annotations

from typing import Dict, Any, List
import datetime as dt


class RightsizingRecommender:
    def recommend(self) -> Dict[str, Any]:
        now = dt.datetime.utcnow().isoformat()
        recs: List[Dict[str, Any]] = [
            {
                "resource_id": "aws:ec2:i-012345",
                "current_type": "m5.4xlarge",
                "suggested_type": "m5.2xlarge",
                "savings_monthly": 120.0,
                "confidence": 0.8,
                "reason": "CPU < 20% p95, mem < 40% p95",
                "dry_run": True,
            },
            {
                "resource_id": "gcp:sql:instance-99",
                "current_type": "db-custom-8-30720",
                "suggested_type": "db-custom-4-15360",
                "savings_monthly": 210.0,
                "confidence": 0.7,
                "reason": "CPU < 25% p95, IO within limits",
                "dry_run": True,
            },
        ]
        return {
            "generated_at": now,
            "recommendations": recs,
            "total_estimated_savings": sum(r["savings_monthly"] for r in recs),
        }


