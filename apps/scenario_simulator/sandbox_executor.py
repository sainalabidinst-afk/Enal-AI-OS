"""
Sandbox Executor — runs code experiments in an isolated environment.

Leverages the existing Core SandboxRuntime (ADR-001 compliant) to execute
user-provided code or logic in a safe, isolated environment during simulation.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.runtime import SandboxLanguage, sandbox_runtime

logger = logging.getLogger(__name__)


class SandboxExecutor:
    """
    Executes code experiments in the Core SandboxRuntime.

    Usage::

        executor = SandboxExecutor()
        log = executor.execute_experiment("python", "print(42)", input_state)
    """

    def __init__(self) -> None:
        self._sandbox = sandbox_runtime

    async def execute_experiment(
        self,
        language: str,
        code: str,
        input_state: dict[str, Any] | None = None,
        timeout_seconds: int = 30,
    ) -> dict[str, Any]:
        """
        Execute a code experiment in the sandbox.

        Args:
            language: "python" or "bash".
            code: The code to execute.
            input_state: Optional state variables injected as environment.
            timeout_seconds: Maximum execution time.

        Returns:
            Sandbox log entry with result, error, and timing.
        """
        lang = SandboxLanguage.PYTHON if language == "python" else SandboxLanguage.BASH

        # Inject input state as environment variables in the code
        injected_code = self._inject_state(code, input_state or {})

        start = time.monotonic()
        result = await self._sandbox.execute(
            language=lang,
            code=injected_code,
        )
        duration_ms = (time.monotonic() - start) * 1000

        log_entry = {
            "id": result.id,
            "language": lang.value,
            "code_snippet": code[:200] + "..." if len(code) > 200 else code,
            "input_state": input_state,
            "result": result.result,
            "error": result.error,
            "exit_code": result.exit_code,
            "duration_ms": round(duration_ms, 2),
            "timestamp": time.time(),
        }

        logger.info(f"Sandbox experiment {result.id}: exit={result.exit_code}, {duration_ms:.1f}ms")
        return log_entry

    def _inject_state(self, code: str, state: dict[str, Any]) -> str:
        """Inject state variables into the code as Python globals."""
        if not state:
            return code

        injection_lines = ["# Injected state variables"]
        for key, value in state.items():
            if isinstance(value, str):
                injection_lines.append(f'{key} = "{value}"')
            elif isinstance(value, bool):
                injection_lines.append(f"{key} = {value}")
            elif isinstance(value, (int, float)):
                injection_lines.append(f"{key} = {value}")
            elif isinstance(value, dict):
                import json as _json
                injection_lines.append(f"{key} = {_json.dumps(value)}")
            else:
                injection_lines.append(f"{key} = {repr(value)}")
        injection_lines.append("")

        return "\n".join(injection_lines) + code

    async def run_sandbox_batch(
        self,
        code: str,
        states: list[dict[str, Any]],
        language: str = "python",
    ) -> list[dict[str, Any]]:
        """Run the same code against multiple input states."""
        results: list[dict[str, Any]] = []
        for state in states:
            log = await self.execute_experiment(language, code, state)
            results.append(log)
        return results
