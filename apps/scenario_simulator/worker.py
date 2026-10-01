"""
Scenario Simulator Worker — thin adapter (per ADR-003).

Routes task requests to the Scenario Simulator Domain Engine.
Does not own business logic; delegates to ScenarioSimulatorEngine.
"""

from __future__ import annotations

from typing import Any

from apps.scenario_simulator.engine import ScenarioSimulatorEngine
from apps.scenario_simulator.schemas import ScenarioRequest, VariableChange

logger: Any = None  # logging.getLogger(__name__) would need import


class ScenarioSimulatorWorker:
    """
    Thin Worker adapter for the Scenario Simulator Capability Pack.

    Responsibilities:
        - Parse incoming task into ScenarioRequest
        - Delegate to ScenarioSimulatorEngine.run_simulation()
        - Return SimulationResult as dict

    Usage::

        worker = ScenarioSimulatorWorker()
        result = await worker.execute(task)
    """

    def __init__(self, engine: ScenarioSimulatorEngine | None = None) -> None:
        self._engine = engine or ScenarioSimulatorEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a scenario simulation task.

        Expected task format::

            {
                "description": "If interest rate rises 1%...",
                "base_state": {"interest_rate": 0.05, ...},
                "iterations": 100,
                "seed": 42,
                "sandbox_code": "return base_state['interest_rate'] * 100",
                "use_llm": false,
                "outcome_fn": "...",  # optional callable
            }

        Returns:
            SimulationResult as a JSON-serializable dict.
        """
        # Build scenario request
        description = task.get("description", task.get("intent", ""))
        base_state = task.get("base_state", task.get("context", {}))

        request = self._build_request(task, description, base_state)

        outcome_fn = task.get("outcome_fn")
        result = await self._engine.run_simulation_async(request, outcome_fn=outcome_fn)
        return result.to_dict()

    def execute_sync(self, task: dict[str, Any]) -> dict[str, Any]:
        """Synchronous variant for non-async contexts."""
        description = task.get("description", task.get("intent", ""))
        base_state = task.get("base_state", task.get("context", {}))
        request = self._build_request(task, description, base_state)
        result = self._engine.run_simulation(request, outcome_fn=task.get("outcome_fn"))
        return result.to_dict()

    def simulate_plan(self, plan: list[dict[str, Any]], context: dict[str, Any]) -> dict[str, Any]:
        """Simulate a plan under variable conditions."""
        result = self._engine.simulate_plan(plan, context)
        return result.to_dict()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_request(
        self, task: dict[str, Any], description: str, base_state: dict[str, Any]
    ) -> ScenarioRequest:
        """Build a ScenarioRequest from a task dict."""
        variable_changes = []
        for vc in task.get("variable_changes", []):
            if isinstance(vc, dict):
                variable_changes.append(VariableChange(**{
                    k: v for k, v in vc.items() if k in VariableChange.model_fields
                }))

        # If no explicit changes but description has them, use builder
        if not variable_changes and description:
            self._engine.builder.build(description, base_state, task.get("iterations", 100), task.get("seed"))

        return ScenarioRequest(
            title=task.get("title", f"Scenario: {description[:50]}"),
            description=description,
            base_state=base_state or {},
            variable_changes=variable_changes,
            iterations=task.get("iterations", 100),
            seed=task.get("seed"),
            sandbox_enabled=task.get("sandbox_enabled", False),
            sandbox_code=task.get("sandbox_code"),
            context=task.get("context", {}),
        )
