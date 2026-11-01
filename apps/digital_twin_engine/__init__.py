"""
Digital Twin Engine — simulation brain for Decision Intelligence.

Provides DigitalTwinEngine for state mirroring, scenario simulation,
adversarial red-team audits, and causal inference by composing
ScenarioSimulatorEngine, AdversarialTestingEngine, and CrossDomainGraphEngine.
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.digital_twin_engine.engine import DigitalTwinEngine
from apps.digital_twin_engine.schemas import (
    CausalTrace,
    RedTeamAuditResult,
    SimulationRequest,
    SimulationResult,
    TwinState,
    TwinStatus,
)
from apps.digital_twin_engine.worker import DigitalTwinWorker


class DigitalTwinApp(BaseReferenceApp):
    """Expose the Digital Twin worker through the capability app contract."""

    name = "digital-twin-engine"
    version = "1.0.0"
    description = "Digital Twin Engine for Decision Intelligence — simulation brain"
    category = "decision-intelligence"
    pipeline = ["perception", "memory", "reasoning", "simulation", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DigitalTwinWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        if user_input and "scenario" not in task:
            task["scenario"] = user_input
        return await self.worker.execute(task)


def get_app() -> DigitalTwinApp:
    """Return a Digital Twin app that conforms to the capability contract."""
    return DigitalTwinApp()


__all__ = [
    "get_app",
    "DigitalTwinApp",
    "DigitalTwinEngine",
    "DigitalTwinWorker",
    "TwinState",
    "TwinStatus",
    "SimulationRequest",
    "SimulationResult",
    "CausalTrace",
    "RedTeamAuditResult",
]
