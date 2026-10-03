"""
Scenario Simulator — Real-Time Simulation & Sandboxing Module.

Capability Pack for predictive What-If scenario analysis using Monte Carlo
simulation with sandboxed code execution.

Pipeline:
    ScenarioRequest
        ↓
    ScenarioBuilder (parse natural language → structured scenario)
        ↓
    MonteCarloRunner (N iterations with distribution sampling)
        ↓
    SandboxExecutor (optional isolated code experiments)
        ↓
    OutcomeAnalyzer (distribution, best/worst/most-likely, statistics)
        ↓
    SimulationResult
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.scenario_simulator.engine import ScenarioSimulatorEngine
from apps.scenario_simulator.schemas import (
    BaseVariable,
    ChangeType,
    DistributionType,
    OutcomeResult,
    OutcomeType,
    ScenarioRequest,
    SimulationResult,
    VariableChange,
    VariableType,
)
from apps.scenario_simulator.worker import ScenarioSimulatorWorker


class ScenarioSimulatorApp(BaseReferenceApp):
    name = "scenario-simulator"
    version = "1.0.0"
    description = "Real-time What-If scenario simulation with Monte Carlo analysis and sandboxing"
    category = "simulation"
    pipeline = ["perception", "memory", "reasoning", "simulation", "decision"]

    def __init__(self) -> None:
        self.worker = ScenarioSimulatorWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("description", user_input)
        return await self.worker.execute(task)

    def run_sync(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("description", user_input)
        return self.worker.execute_sync(task)


def get_app() -> ScenarioSimulatorApp:
    return ScenarioSimulatorApp()


__all__ = [
    "ScenarioSimulatorApp",
    "get_app",
    "ScenarioSimulatorEngine",
    "ScenarioSimulatorWorker",
    "ScenarioRequest",
    "SimulationResult",
    "VariableChange",
    "BaseVariable",
    "ChangeType",
    "DistributionType",
    "VariableType",
    "OutcomeType",
    "OutcomeResult",
]
