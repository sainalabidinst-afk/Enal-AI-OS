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
from backend.app.core.model_router import model_router

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

            system_prompt = validated.prompt or "You are a helpful assistant."
            user_message = task or context.get("user_input", "") if context else task or ""
            if not user_message:
                user_message = "Process the request based on your instructions."

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]

            try:
                response = await model_router.acomplete(
                    messages,
                    temperature=validated.temperature,
                    max_tokens=validated.max_tokens,
                    model=validated.model,
                )
                result_text = response.choices[0].message.content if response else ""
                if not result_text:
                    result_text = "Agent executed but returned empty response."
            except Exception as llm_exc:
                logger.error("LLM call failed for agent %s: %s", validated.name, llm_exc)
                return {
                    "success": False,
                    "error": f"LLM execution failed: {llm_exc}",
                    "agent_id": validated.id,
                    "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                }

            latency_ms = round((time.perf_counter() - started) * 1000, 2)
            return {
                "success": True,
                "agent_id": validated.id,
                "name": validated.name,
                "model": validated.model,
                "task": task,
                "result": result_text,
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
