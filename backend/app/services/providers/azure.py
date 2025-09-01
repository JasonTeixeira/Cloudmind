from __future__ import annotations

from typing import Any, Dict, List

from .base import ProviderClient, ProviderName
from app.utils.retry import async_with_retries, TransientError


class AzureProvider(ProviderClient):
    name = ProviderName.AZURE

    async def discover_resources(self) -> List[Dict[str, Any]]:
        async def _op():
            # Minimal normalized sample; replace with Azure SDK calls
            return [
                {
                    "type": "vm_instance",
                    "id": "azure-vm-001",
                    "name": "vm-eastus-01",
                    "region": "eastus",
                    "state": "running",
                    "metadata": {},
                }
            ]

        return await async_with_retries(_op, attempts=3, retry_on=(TransientError,))

    async def collect_metrics(self, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        async def _op():
            metrics: Dict[str, Any] = {}
            for r in resources:
                metrics[r["id"]] = {"cpu_avg": 25.0, "cpu_p95": 60.0}
            return metrics

        return await async_with_retries(_op, attempts=3, retry_on=(TransientError,))


