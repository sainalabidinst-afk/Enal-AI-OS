"""
Data Engineer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.data_engineer.engine import DataEngineerEngine
from apps.data_engineer.worker import DataEngineerWorker
from apps.data_engineer.schemas import (
    DataEngineeringRequest,
    DataEngineeringReport,
    JobType,
    SourceType,
    Operation,
    QualityRule,
    IssueType,
    IssueSeverity,
    JobStatus,
    FeatureType,
    ChangeType,
    DataSource,
    TransformOperation,
    QualityRuleSpec,
    QualityIssue,
    QualityReport,
    SchemaChange,
    SchemaDriftReport,
    FeatureSpec,
    TimeSeriesReport,
    DatasetSummary,
    DataLineage,
    DataQualityRecord,
)


class DataEngineerApp(BaseReferenceApp):
    name = "data-engineer"
    version = "1.0.0"
    description = "Data processing, quality, transformation, and feature engineering"
    category = "data"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DataEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> DataEngineerApp:
    return DataEngineerApp()

__all__ = [
    "DataEngineerApp",
    "get_app",
    "DataEngineerEngine",
    "DataEngineerWorker",
    "DataEngineeringRequest",
    "DataEngineeringReport",
    "JobType",
    "SourceType",
    "Operation",
    "QualityRule",
    "IssueType",
    "IssueSeverity",
    "JobStatus",
    "FeatureType",
    "ChangeType",
    "DataSource",
    "TransformOperation",
    "QualityRuleSpec",
    "QualityIssue",
    "QualityReport",
    "SchemaChange",
    "SchemaDriftReport",
    "FeatureSpec",
    "TimeSeriesReport",
    "DatasetSummary",
    "DataLineage",
    "DataQualityRecord",
]
