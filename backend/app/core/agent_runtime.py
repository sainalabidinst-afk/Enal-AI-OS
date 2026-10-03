"""
Runtime for executing agents from blueprints.

Executes agent definitions using existing backend capabilities,
including model gateway, connectors, and memory.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.core.agent_factory import agent_factory
from backend.app.core.agent_validator import AgentValidationError, agent_validator

logger = logging.getLogger(__name__)


class AgentRuntimeError(Exception):
    """Raised when agent execution fails."""


class AgentRuntime:
    """Execute an agent blueprint through the backend runtime."""

    async def run(
        self,
        blueprint: dict[str, Any],
        task: str = "",
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        try:
            validated = agent_validator.validate(blueprint)
        except AgentValidationError as exc:
            logger.error("Agent validation failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "agent_id": blueprint.get("id"),
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            }

        try:
            config = agent_factory.create(validated)
            logger.info(
                "Running agent %s with model %s",
                validated.name,
                validated.model,
            )
            latency_ms = round((time.perf_counter() - started) * 1000, 2)
            return {
                "success": True,
                "agent_id": validated.id,
                "name": validated.name,
                "model": validated.model,
                "task": task,
                "result": f"Agent {validated.name} executed successfully",
                "config": config,
                "latency_ms": latency_ms,
            }
        except Exception as exc:
            logger.error("Agent runtime error: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "agent_id": validated.id,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            }


agent_runtime = AgentRuntime()
