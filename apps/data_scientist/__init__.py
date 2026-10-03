"""
Data Scientist Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.data_scientist.engine import DataScientistEngine
from apps.data_scientist.schemas import (
    BusinessContext,
    DataScientistInputs,
    DataScientistOperation,
    DataScientistRecord,
    DataScientistReport,
    DataScientistRequest,
    FeatureImportance,
    ModelEvaluation,
    PipelineResult,
    TrainingSummary,
)
from apps.data_scientist.worker import DataScientistWorker


class DataScientistApp(BaseReferenceApp):
    name = "data-scientist"
    version = "2.7.0"
    description = (
        "Advanced ML pipelines, feature engineering, model training, "
        "evaluation, and feature importance analysis"
    )
    category = "ai"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DataScientistWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> DataScientistApp:
    return DataScientistApp()


__all__ = [
    "DataScientistApp",
    "get_app",
    "DataScientistEngine",
    "DataScientistWorker",
    "DataScientistRequest",
    "DataScientistReport",
    "DataScientistOperation",
    "DataScientistInputs",
    "DataScientistRecord",
    "TrainingSummary",
    "ModelEvaluation",
    "FeatureImportance",
    "PipelineResult",
    "BusinessContext",
]
