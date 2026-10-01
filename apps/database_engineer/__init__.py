"""
Database Engineer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.database_engineer.engine import DatabaseEngineerEngine
from apps.database_engineer.schemas import (
    BackupPlan,
    ColumnDefinition,
    DatabaseAnalysisRecord,
    DatabaseReport,
    DatabaseRequest,
    DatabaseType,
    Finding,
    FindingCategory,
    ForeignKey,
    IndexRecommendation,
    MigrationPlan,
    MigrationStep,
    OperationType,
    PerformanceStats,
    ReplicationDesign,
    SchemaDefinition,
    SchemaRecommendation,
    Severity,
    TableDefinition,
    WorkloadProfile,
)
from apps.database_engineer.worker import DatabaseEngineerWorker


class DatabaseEngineerApp(BaseReferenceApp):
    name = "database-engineer"
    version = "1.0.0"
    description = "Database design, optimization, migration, and resilience planning"
    category = "database"
    pipeline = ["perception", "analysis", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DatabaseEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> DatabaseEngineerApp:
    return DatabaseEngineerApp()

__all__ = [
    "DatabaseEngineerApp",
    "get_app",
    "DatabaseEngineerEngine",
    "DatabaseEngineerWorker",
    "DatabaseRequest",
    "DatabaseReport",
    "DatabaseType",
    "OperationType",
    "Severity",
    "FindingCategory",
    "ColumnDefinition",
    "ForeignKey",
    "TableDefinition",
    "SchemaDefinition",
    "WorkloadProfile",
    "Finding",
    "SchemaRecommendation",
    "IndexRecommendation",
    "MigrationStep",
    "MigrationPlan",
    "ReplicationDesign",
    "BackupPlan",
    "PerformanceStats",
    "DatabaseAnalysisRecord",
]
