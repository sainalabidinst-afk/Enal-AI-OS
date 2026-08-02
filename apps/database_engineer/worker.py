"""
Database Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the Database Engineer Domain Engine.
Does not own business logic; delegates to DatabaseEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.database_engineer.engine import DatabaseEngineerEngine
from apps.database_engineer.schemas import (
    DatabaseRequest,
    DatabaseType,
    OperationType,
    SchemaDefinition,
    WorkloadProfile,
    TableDefinition,
    ColumnDefinition,
    ForeignKey,
)


class DatabaseEngineerWorker:
    """
    Thin Worker adapter for the Database Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into DatabaseRequest
        - Delegate to DatabaseEngineerEngine.analyze()
        - Return DatabaseReport as dict

    Usage::

        worker = DatabaseEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: DatabaseEngineerEngine | None = None) -> None:
        self._engine = engine or DatabaseEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a database engineering task.

        Expected task format::

            {
                "operation": "schema_design",
                "database_type": "postgresql",
                "schema": {"tables": [...]},
                "queries": ["SELECT ..."],
                "workload_profile": {...}
            }

        Returns:
            DatabaseReport as a JSON-serializable dict.
        """
        op_value = task.get("operation", "schema_design")
        db_value = task.get("database_type", "postgresql")

        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.schema_design

        try:
            database_type = DatabaseType(db_value)
        except ValueError:
            database_type = DatabaseType.postgresql

        schema_data = task.get("schema")
        schema = None
        if schema_data:
            tables = []
            for t in schema_data.get("tables", []):
                columns = [ColumnDefinition(**c) for c in t.get("columns", [])]
                fks = [ForeignKey(**fk) for fk in t.get("foreign_keys", [])]
                tables.append(TableDefinition(
                    name=t["name"],
                    columns=columns,
                    primary_key=t.get("primary_key", []),
                    foreign_keys=fks,
                ))
            schema = SchemaDefinition(tables=tables)

        workload = None
        if task.get("workload_profile"):
            workload = WorkloadProfile(**task["workload_profile"])

        request = DatabaseRequest(
            operation=operation,
            database_type=database_type,
            schema=schema,
            queries=task.get("queries", []),
            workload_profile=workload,
            current_schema_version=task.get("current_schema_version", "v1"),
            target_schema_version=task.get("target_schema_version", "v2"),
            rto_hours=task.get("rto_hours", 4.0),
            rpo_minutes=task.get("rpo_minutes", 60),
        )

        report = self._engine.analyze(request)
        return report.to_dict()
