"""
Innovation Strategist Pack
=========================

Demonstrates ECP capabilities for innovation strategy and technology foresight.

Workflow:
    User Request
        ↓
    Intent Router
        ↓
    Capability Graph → innovation-strategist-*
        ↓
    Task Planner
        ↓
    Subtasks:
    - Trend Analysis
    - Technology Forecast
    - Competitive Intelligence
    - Scenario Planning
    - Opportunity Identification
        ↓
    Execution Planner
        ↓
    Execution Runtime
        ↓
    Innovation Strategist Worker
        ↓
    Strategy Analysis Engine (full foresight pipeline)
        ↓
    Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.innovation_strategist.engine import InnovationStrategistEngine
from apps.innovation_strategist.schemas import (
    BusinessContext,
    CompetitiveInsight,
    Competitor,
    InnovationConfig,
    InnovationOperation,
    InnovationOpportunity,
    InnovationReport,
    InnovationRequest,
    InnovationStrategistPackRecord,
    Scenario,
    ScenarioLikelihood,
    TechnologyDomain,
    TechnologyForecast,
    TrendCategory,
    TrendDataPoint,
    TrendImpact,
    TrendSignal,
    TrendTimeframe,
)
from apps.innovation_strategist.worker import InnovationStrategistWorker


class InnovationStrategistApp(BaseReferenceApp):
    name = "innovation-strategist"
    version = "1.0.0"
    description = "Innovation strategy and technology foresight: trend analysis, competitive intelligence, scenario planning, and opportunity identification"  # noqa: E501
    category = "strategy"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = InnovationStrategistWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> InnovationStrategistApp:
    return InnovationStrategistApp()


__all__ = [
    "InnovationStrategistApp",
    "InnovationStrategistEngine",
    "InnovationStrategistWorker",
    "InnovationOperation",
    "TrendCategory",
    "TrendImpact",
    "TrendTimeframe",
    "ScenarioLikelihood",
    "TechnologyDomain",
    "TrendDataPoint",
    "Competitor",
    "BusinessContext",
    "InnovationConfig",
    "InnovationRequest",
    "TrendSignal",
    "TechnologyForecast",
    "CompetitiveInsight",
    "Scenario",
    "InnovationOpportunity",
    "InnovationReport",
    "InnovationStrategistPackRecord",
]
