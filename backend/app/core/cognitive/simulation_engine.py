import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from backend.app.core.model_router import model_router
from backend.app.core.sandbox import sandbox_runtime

logger = logging.getLogger(__name__)


class SimulationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    NEEDS_REVISION = "needs_revision"


@dataclass
class SimulationStep:
    id: str
    description: str
    action: str
    expected_result: str
    actual_result: str | None = None
    passed: bool = False
    error: str | None = None


@dataclass
class Simulation:
    id: str
    plan: list[dict[str, Any]]
    steps: list[SimulationStep] = field(default_factory=list)
    status: SimulationStatus = SimulationStatus.PENDING
    failure_points: list[str] = field(default_factory=list)
    improvements: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class SimulationEngine:
    def __init__(self):
        self._simulations: dict[str, Simulation] = {}

    async def run(self, plan: list[dict[str, Any]], dry_run: bool = True) -> Simulation:
        sim_id = f"sim-{len(self._simulations)}"
        simulation = Simulation(id=sim_id, plan=plan)
        for i, step_data in enumerate(plan):
            step = SimulationStep(
                id=f"step-{i}",
                description=step_data.get("description", ""),
                action=step_data.get("action", ""),
                expected_result=step_data.get("expected_result", ""),
            )
            if dry_run:
                step.passed, step.error = await self._dry_run_step(step)
            else:
                step.passed, step.error = await self._execute_step(step)
            simulation.steps.append(step)
            if not step.passed:
                simulation.failure_points.append(step.id)
        if simulation.failure_points:
            simulation.status = SimulationStatus.NEEDS_REVISION
            simulation.improvements = await self._suggest_improvements(simulation)
        else:
            simulation.status = SimulationStatus.SUCCESS
        self._simulations[sim_id] = simulation
        return simulation

    async def _dry_run_step(self, step: SimulationStep) -> tuple[bool, str | None]:
        prompt = (
            f"Simulate the following action and predict if it will succeed.\n"
            f"Action: {step.action}\n"
            f"Description: {step.description}\n"
            f"Expected: {step.expected_result}\n\n"
            "Output JSON: {\"passed\": bool, \"reason\": str}"
        )
        response = await model_router.acomplete([{"role": "user", "content": prompt}], temperature=0.3, max_tokens=256)
        import json
        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("passed", False), result.get("reason")
        except (json.JSONDecodeError, AttributeError):
            return False, "Simulation failed"

    async def _execute_step(self, step: SimulationStep) -> tuple[bool, str | None]:
        try:
            result = await sandbox_runtime.execute(language=__import__("backend.app.core.sandbox", fromlist=["SandboxLanguage"]).SandboxLanguage.PYTHON, code=step.action)
            return result.error is None, result.error
        except Exception as e:
            return False, str(e)

    async def _suggest_improvements(self, simulation: Simulation) -> list[str]:
        failed_steps = [s for s in simulation.steps if not s.passed]
        if not failed_steps:
            return []
        prompt = (
            "The following simulation steps failed. Suggest improvements to the plan.\n\n"
            "Failed steps:\n"
        )
        for step in failed_steps:
            prompt += f"- {step.description}: {step.error}\n"
        prompt += "\nOutput JSON array of improvement suggestions."
        response = await model_router.acomplete([{"role": "user", "content": prompt}], temperature=0.5, max_tokens=512)
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except (json.JSONDecodeError, AttributeError):
            return ["Review failed steps and retry"]


simulation_engine = SimulationEngine()
