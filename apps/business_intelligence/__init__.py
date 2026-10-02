"""
Business Intelligence Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.business_intelligence.engine import BusinessIntelligenceEngine
from apps.business_intelligence.schemas import (
    BusinessContext,
    BusinessIntelligenceInputs,
    BusinessIntelligenceOperation,
    BusinessIntelligenceRecord,
    BusinessIntelligenceReport,
    BusinessIntelligenceRequest,
    DashboardConfig,
    KpiMetric,
    ScenarioAnalysis,
)
from apps.business_intelligence.worker import BusinessIntelligenceWorker


class BusinessIntelligenceApp(BaseReferenceApp):
    name = "business-intelligence"
    version = "2.8.0"
    description = (
        "Dashboarding, KPI tracking, metric analysis, and scenario planning "
        "for business intelligence"
    )
    category = "business"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = BusinessIntelligenceWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> BusinessIntelligenceApp:
    return BusinessIntelligenceApp()


__all__ = [
    "BusinessIntelligenceApp",
    "get_app",
    "BusinessIntelligenceEngine",
    "BusinessIntelligenceWorker",
    "BusinessIntelligenceRequest",
    "BusinessIntelligenceReport",
    "BusinessIntelligenceOperation",
    "BusinessIntelligenceInputs",
    "BusinessIntelligenceRecord",
    "KpiMetric",
    "DashboardConfig",
    "ScenarioAnalysis",
    "BusinessContext",
]
