"""
Schemas for AI-assisted terminal planning and execution
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    goal: str = Field(..., description="High-level goal for the AI to plan")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional context about project/env")


class PlanResponse(BaseModel):
    commands: List[str] = Field(..., description="Safe, planned commands")


class ExecutePlanRequest(BaseModel):
    session_id: str = Field(..., description="Existing terminal session ID")
    commands: List[str] = Field(..., description="Commands to execute (already planned)")


class ExecutePlanResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="Per-command execution results")


