"""
Tool engine for executing tool blueprints.

Runs validated tool step graphs through the backend runtime,
producing structured outputs for each step.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.core.step_executor import step_executor
from backend.app.core.step_validator import StepValidationError, step_validator

logger = logging.getLogger(__name__)


class ToolEngineError(Exception):
    """Raised when tool execution fails."""


class ToolEngine:
    """Execute a tool blueprint step graph."""

    async def run(
        self,
        blueprint: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        try:
            validated = step_validator.validate(blueprint)
        except StepValidationError as exc:
            logger.error("Tool validation failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "tool_id": blueprint.get("id"),
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            }

        steps = validated.get("steps", [])
        results: list[dict[str, Any]] = []

        for step in steps:
            try:
                result = await step_executor.execute(step, context)
                results.append(result)
                if not result.get("success"):
                    break
            except Exception as exc:
                logger.error("Tool engine step error: %s", exc)
                results.append(
                    {
                        "step_id": step.get("id"),
                        "type": step.get("type"),
                        "success": False,
                        "error": str(exc),
                    }
                )
                break

        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "success": all(result.get("success", False) for result in results),
            "tool_id": validated.get("id"),
            "name": validated.get("name"),
            "results": results,
            "latency_ms": latency_ms,
        }


tool_engine = ToolEngine()
