"""
Data Scientist Pack
===================

Demonstrates ECP capabilities for advanced ML pipelines and data science workflows.

Workflow:
    User Request
        ↓
    Intent Router
        ↓
    Capability Graph → data-scientist-*
        ↓
    Task Planner
        ↓
    Subtasks:
    - Feature Engineering
    - Model Training
    - Model Evaluation
    - Hyperparameter Tuning
        ↓
    Execution Planner
        ↓
    Execution Runtime
        ↓
    Data Scientist Worker
        ↓
    ML Pipeline Engine (full ML pipeline)
        ↓
    Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.data_scientist.engine import DataScientistEngine
from apps.data_scientist.schemas import (
    BusinessContext,
    DataScienceConfig,
    DataScienceOperation,
    DataScienceReport,
    DataScienceRequest,
    DataScientistPackRecord,
    Dataset,
    FeatureConfig,
    FeatureEngineeringResult,
    HyperparameterResult,
    MLAlgorithm,
    MLTask,
    ModelConfig,
    ModelEvaluationResult,
    ModelTrainingResult,
)
from apps.data_scientist.worker import DataScientistWorker


class DataScientistApp(BaseReferenceApp):
    name = "data-scientist"
    version = "1.0.0"
    description = "Advanced ML pipelines: feature engineering, model training, evaluation, and hyperparameter tuning"  # noqa: E501
    category = "data-science"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DataScientistWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> DataScientistApp:
    return DataScientistApp()


__all__ = [
    "DataScientistApp",
    "DataScientistEngine",
    "DataScientistWorker",
    "MLTask",
    "MLAlgorithm",
    "DataScienceOperation",
    "Dataset",
    "FeatureConfig",
    "ModelConfig",
    "BusinessContext",
    "DataScienceConfig",
    "DataScienceRequest",
    "FeatureEngineeringResult",
    "ModelTrainingResult",
    "ModelEvaluationResult",
    "HyperparameterResult",
    "DataScienceReport",
    "DataScientistPackRecord",
]
