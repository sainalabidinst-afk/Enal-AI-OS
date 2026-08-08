"""
Business Analyst — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.business_analyst.engine import BusinessAnalystEngine
from apps.business_analyst.worker import BusinessAnalystWorker
from apps.business_analyst.schemas import (
    BusinessAnalysisRequest,
    BusinessAnalysisReport,
    OperationType,
    RequirementType,
    Priority,
    StoryPoint,
    ProcessActivityType,
    OutputFormat,
    BusinessContext,
    StakeholderInput,
    Persona,
    QualityAttributes,
    Requirement,
    UserStory,
    UseCase,
    ProcessActivity,
    ProcessModel,
    GapItem,
    ROIResult,
    ProcessOptimization,
    BusinessAnalysisRecord,
)


class BusinessAnalystApp(BaseReferenceApp):
    name = "business-analyst"
    version = "1.0.0"
    description = "Business requirements analysis and process optimization"
    category = "business"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = BusinessAnalystWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> BusinessAnalystApp:
    return BusinessAnalystApp()

__all__ = [
    "BusinessAnalystApp",
    "get_app",
    "BusinessAnalystEngine",
    "BusinessAnalystWorker",
    "BusinessAnalysisRequest",
    "BusinessAnalysisReport",
    "OperationType",
    "RequirementType",
    "Priority",
    "StoryPoint",
    "ProcessActivityType",
    "OutputFormat",
    "BusinessContext",
    "StakeholderInput",
    "Persona",
    "QualityAttributes",
    "Requirement",
    "UserStory",
    "UseCase",
    "ProcessActivity",
    "ProcessModel",
    "GapItem",
    "ROIResult",
    "ProcessOptimization",
    "BusinessAnalysisRecord",
]
