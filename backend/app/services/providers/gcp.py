from __future__ import annotations

from typing import Any, Dict, List

from .base import ProviderClient, ProviderName
from app.utils.retry import async_with_retries, TransientError


class GCPProvider(ProviderClient):
    name = ProviderName.GCP

    async def discover_resources(self) -> List[Dict[str, Any]]:
        async def _op():
            # Minimal normalized sample; replace with GCP SDK calls
            return [
                {
                    "type": "compute_instance",
                    "id": "gcp-vm-001",
                    "name": "vm-uscentral1-01",
                    "region": "us-central1",
                    "state": "RUNNING",
                    "metadata": {},
                }
            ]

        return await async_with_retries(_op, attempts=3, retry_on=(TransientError,))

    async def collect_metrics(self, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        async def _op():
            metrics: Dict[str, Any] = {}
            for r in resources:
                metrics[r["id"]] = {"cpu_avg": 20.0, "cpu_p95": 50.0}
            return metrics

        return await async_with_retries(_op, attempts=3, retry_on=(TransientError,))


