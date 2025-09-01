from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ProviderName(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


@dataclass
class ProviderError:
    provider: ProviderName
    code: str
    message: str
    retryable: bool


class ProviderClient:
    """Abstract interface for cloud provider discovery and metrics."""

    name: ProviderName

    async def discover_resources(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    async def collect_metrics(self, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        raise NotImplementedError


