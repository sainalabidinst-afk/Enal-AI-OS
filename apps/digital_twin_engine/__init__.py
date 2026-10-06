"""
Digital Twin Engine — simulation brain for Decision Intelligence.

Provides DigitalTwinEngine for state mirroring, scenario simulation,
adversarial red-team audits, and causal inference by composing
ScenarioSimulatorEngine, AdversarialTestingEngine, and CrossDomainGraphEngine.
"""

from typing import Any

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


def get_app() -> dict[str, Any] | None:
    """Return Digital Twin Engine app metadata."""
    return {
        "name": "digital-twin-engine",
        "version": "1.0.0",
        "description": "Digital Twin Engine for Decision Intelligence — simulation brain",
        "category": "decision-intelligence",
        "pipeline": ["perception", "memory", "reasoning", "simulation", "decision", "action"],
    }


__all__ = [
    "get_app",
    "DigitalTwinEngine",
    "DigitalTwinWorker",
    "TwinState",
    "TwinStatus",
    "SimulationRequest",
    "SimulationResult",
    "CausalTrace",
    "RedTeamAuditResult",
]
