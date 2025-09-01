import asyncio

import pytest

from app.services.providers.azure import AzureProvider
from app.services.providers.gcp import GCPProvider


@pytest.mark.asyncio
async def test_azure_provider_minimal():
    p = AzureProvider()
    res = await p.discover_resources()
    assert isinstance(res, list)
    metrics = await p.collect_metrics(res)
    assert isinstance(metrics, dict)


@pytest.mark.asyncio
async def test_gcp_provider_minimal():
    p = GCPProvider()
    res = await p.discover_resources()
    assert isinstance(res, list)
    metrics = await p.collect_metrics(res)
    assert isinstance(metrics, dict)


