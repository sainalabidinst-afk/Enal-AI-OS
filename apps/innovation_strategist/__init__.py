"""
Innovation Strategist Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.innovation_strategist.engine import InnovationStrategistEngine
from apps.innovation_strategist.schemas import (
    BusinessContext,
    ForesightScenario,
    InnovationStrategistInputs,
    InnovationStrategistOperation,
    InnovationStrategistRecord,
    InnovationStrategistReport,
    InnovationStrategistRequest,
    PortfolioItem,
    TechTrend,
)
from apps.innovation_strategist.worker import InnovationStrategistWorker


class InnovationStrategistApp(BaseReferenceApp):
    name = "innovation-strategist"
    version = "2.9.0"
    description = (
        "Trend analysis, technology foresight, R&D portfolio planning, "
        "and strategic scenario modeling"
    )
    category = "strategy"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = InnovationStrategistWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> InnovationStrategistApp:
    return InnovationStrategistApp()


__all__ = [
    "InnovationStrategistApp",
    "get_app",
    "InnovationStrategistEngine",
    "InnovationStrategistWorker",
    "InnovationStrategistRequest",
    "InnovationStrategistReport",
    "InnovationStrategistOperation",
    "InnovationStrategistInputs",
    "InnovationStrategistRecord",
    "PortfolioItem",
    "TechTrend",
    "ForesightScenario",
    "BusinessContext",
]
