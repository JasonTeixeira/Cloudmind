"""
Commitment planner (MVP): computes simple coverage/gap and proposes purchase plan
for Savings Plans/Reserved Instances / Committed Use (simulated numbers).
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import datetime as dt


class CommitmentPlanner:
    def plan(self, lookback_days: int = 30, target_coverage: float = 0.7) -> Dict[str, Any]:
        now = dt.datetime.utcnow().isoformat()
        baseline_spend = 10000.0
        covered = baseline_spend * 0.45
        gap = max(0.0, baseline_spend * target_coverage - covered)
        proposal = {
            "provider": "aws",
            "instrument": "savings_plan",
            "term_years": 1,
            "payment_option": "no_upfront",
            "hourly_commit": round(gap / (30 * 24), 2),
            "estimated_savings_pct": 0.18,
            "risk_notes": "Assumes steady-state usage; exclude spiky/batch workloads.",
        }
        return {
            "generated_at": now,
            "lookback_days": lookback_days,
            "target_coverage": target_coverage,
            "baseline_spend": baseline_spend,
            "covered": covered,
            "gap": gap,
            "proposal": proposal,
        }


