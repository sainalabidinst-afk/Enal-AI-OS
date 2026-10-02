"""
HSE Specialist — __init__.py
"""

from typing import Any

from apps.hse_specialist.engine import HSESpecialistEngine
from apps.hse_specialist.schemas import (
    BusinessContext,
    ControlReviewResult,
    HazardFinding,
    HSEInputs,
    HSEOperation,
    HSESpecialistRecord,
    HSESpecialistReport,
    HSESpecialistRequest,
    IncidentAnalysis,
    RiskScore,
)
from apps.hse_specialist.worker import HSESpecialistWorker
from apps.base import BaseReferenceApp


class HSESpecialistApp(BaseReferenceApp):
    name = "hse-specialist"
    version = "1.0.0"
    description = "Hazard identification, risk assessment, control review, and incident analysis for safety operations"
    category = "safety"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = HSESpecialistWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> HSESpecialistApp:
    return HSESpecialistApp()


__all__ = [
    "HSESpecialistApp",
    "get_app",
    "HSESpecialistEngine",
    "HSESpecialistWorker",
    "HSESpecialistRequest",
    "HSESpecialistReport",
    "HSEOperation",
    "HSEInputs",
    "HazardFinding",
    "RiskScore",
    "ControlReviewResult",
    "IncidentAnalysis",
    "BusinessContext",
    "HSESpecialistRecord",
]
