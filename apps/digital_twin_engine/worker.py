"""
Digital Twin Engine Worker — thin adapter (per ADR-003).

Routes task requests to the Digital Twin Domain Engine.
Does not own business logic; delegates to DigitalTwinEngine.
"""

from __future__ import annotations

from typing import Any

from apps.digital_twin_engine.engine import DigitalTwinEngine
from apps.digital_twin_engine.schemas import SimulationRequest

logger: Any = None


class DigitalTwinWorker:
    """
    Thin Worker adapter for the Digital Twin Capability Pack.

    Responsibilities:
        - Parse incoming task into engine method calls
        - Delegate to DigitalTwinEngine
        - Return results as JSON-serializable dicts

    Usage::

        worker = DigitalTwinWorker()
        result = await worker.execute(task)
    """

    def __init__(self, engine: DigitalTwinEngine | None = None) -> None:
        self._engine = engine or DigitalTwinEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a digital twin task.

        Expected task format::

            {
                "action": "simulate" | "red_team" | "causal_trace" | "status" | "mirror",
                ...
            }

        Returns:
            Result dict from the engine.
        """
        action = task.get("action", "status")
        if action == "mirror":
            state = task.get("system_state", {})
            twin = self._engine.mirror_state(state)
            return twin.model_dump()
        if action == "simulate":
            request = self._build_simulation_request(task)
            result = self._engine.run_simulation(
                scenario=request.scenario,
                parameters=request.parameters,
                iterations=request.iterations,
            )
            return result.model_dump()
        if action == "red_team":
            subject = task.get("subject", "")
            subject_type = task.get("subject_type", "plan")
            result = self._engine.run_red_team(subject=subject, subject_type=subject_type)
            return result.model_dump()
        if action == "causal_trace":
            treatment = task.get("treatment", "")
            outcome = task.get("outcome", "")
            conditions = task.get("conditions")
            result = self._engine.run_causal_trace(
                treatment=treatment, outcome=outcome, conditions=conditions
            )
            return result.model_dump()
        status = self._engine.get_status()
        return status.model_dump()

    def execute_sync(self, task: dict[str, Any]) -> dict[str, Any]:
        """Synchronous variant for non-async contexts."""
        import asyncio

        return asyncio.run(self.execute(task))

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_simulation_request(self, task: dict[str, Any]) -> SimulationRequest:
        """Build a SimulationRequest from a task dict."""
        return SimulationRequest(
            simulation_id=task.get("simulation_id"),
            scenario=task.get("scenario", ""),
            parameters=task.get("parameters", {}),
            iterations=task.get("iterations", 100),
            time_warp_factor=task.get("time_warp_factor", 1.0),
            status="running",
        )
