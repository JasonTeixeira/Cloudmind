"""
AI-Assisted Terminal Service
Plans commands with LLMs and executes with strict safety guardrails
"""

from __future__ import annotations

import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.core.config import settings
from app.services.terminal.terminal_service import terminal_service


logger = logging.getLogger(__name__)


class AITerminalService:
    def __init__(self) -> None:
        # No heavy AI imports at module import time; keep this lightweight for tests
        pass

    def _is_enabled(self) -> bool:
        return bool(getattr(settings, "ENABLE_AI_TERMINAL", False))

    def _is_command_allowed(self, command: str) -> bool:
        cmd = command.strip()
        # Block dangerous patterns first
        for pattern in settings.AI_TERMINAL_BLOCKED_PATTERNS:
            if pattern in cmd:
                return False
        # Require allowed prefixes
        for prefix in settings.AI_TERMINAL_ALLOWED_COMMAND_PREFIXES:
            if cmd.startswith(prefix):
                return True
        return False

    async def plan_commands(self, goal: str, context: Dict[str, Any] | None = None) -> List[str]:
        if not self._is_enabled():
            raise RuntimeError("AI terminal is disabled")
        text = (goal or "").lower()
        planned: List[str] = []
        # Simple heuristic planner with safe defaults
        if any(k in text for k in ["list", "files", "dir", "explore", "browse"]):
            planned.extend(["pwd", "ls -la"])
        if any(k in text for k in ["git", "repo", "branch", "commits"]):
            planned.append("git status")
            planned.append("git log --oneline -n 10")
        if any(k in text for k in ["k8s", "kubernetes", "cluster", "pods", "deployments"]):
            planned.append("kubectl cluster-info")
            planned.append("kubectl get nodes")
            planned.append("kubectl get pods -A")
        if any(k in text for k in ["helm", "chart"]):
            planned.append("helm list -A")
        if any(k in text for k in ["terraform", "iac", "infra as code"]):
            planned.append("terraform init -input=false -no-color")
            planned.append("terraform plan -no-color")
        if any(k in text for k in ["python", "pip", "packages", "deps", "dependencies"]):
            planned.append("python -V")
            planned.append("pip list")
        if not planned:
            planned = ["pwd", "ls -la"]
        # Filter with allowlist/policy
        planned = [c for c in planned if self._is_command_allowed(c)]
        if not planned:
            planned = ["pwd", "ls -la"]
        return planned

    async def execute_planned(self, session_id: str, commands: List[str]) -> List[Dict[str, Any]]:
        if not self._is_enabled():
            raise RuntimeError("AI terminal is disabled")
        results: List[Dict[str, Any]] = []
        for cmd in commands:
            if not self._is_command_allowed(cmd):
                results.append({"command": cmd, "skipped": True, "reason": "blocked by policy"})
                continue
            try:
                result = await terminal_service.execute_command(session_id=session_id, command=cmd)
                results.append({
                    "command": cmd,
                    "success": result.success,
                    "exit_code": result.exit_code,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "execution_time": result.execution_time,
                })
            except Exception as e:
                results.append({"command": cmd, "success": False, "error": str(e)})
        return results


ai_terminal_service = AITerminalService()


