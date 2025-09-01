"""
Normalized cost models (MVP) used by the cost pipeline to persist events and allocations.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class CostEvent(Base):
    __tablename__ = "cost_events"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider = Column(String(20), nullable=False)
    account = Column(String(128))
    project_id = Column(String(128))
    service = Column(String(128))
    region = Column(String(64))
    usage_amount = Column(Float, nullable=False, default=0.0)
    cost = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), nullable=False, default="USD")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    tags = Column(JSON, default=dict, nullable=False)


class CostAllocation(Base):
    __tablename__ = "cost_allocations"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    key = Column(String(128), nullable=False)  # e.g., project/customer/environment
    value = Column(String(256), nullable=False)
    cost_total = Column(Float, nullable=False, default=0.0)
    usage_total = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), nullable=False, default="USD")
    period = Column(String(32), nullable=False, default="last_30d")
    allocation_metadata = Column(JSON, default=dict, nullable=False)

