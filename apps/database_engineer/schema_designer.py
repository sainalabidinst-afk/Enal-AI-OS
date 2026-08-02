"""
Database Engineer — Schema Designer.

Analyzes and recommends optimized database schema designs
with appropriate data types, normalization, and constraints.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.database_engineer.schemas import (
    SchemaDefinition,
    TableDefinition,
    ColumnDefinition,
    DatabaseType,
    SchemaRecommendation,
    Severity,
)

logger = logging.getLogger(__name__)


# Recommended data types per database.
_TYPE_RECOMMENDATIONS: dict[str, dict[str, str]] = {
    "postgresql": {
        "id": "SERIAL PRIMARY KEY",
        "uuid": "UUID DEFAULT gen_random_uuid()",
        "string_short": "VARCHAR(255)",
        "string_long": "TEXT",
        "integer": "INTEGER",
        "bigint": "BIGINT",
        "float": "REAL",
        "decimal": "NUMERIC(10,2)",
        "boolean": "BOOLEAN",
        "datetime": "TIMESTAMP WITH TIME ZONE",
        "json": "JSONB",
        "blob": "BYTEA",
    },
    "mysql": {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "uuid": "CHAR(36)",
        "string_short": "VARCHAR(255)",
        "string_long": "TEXT",
        "integer": "INT",
        "bigint": "BIGINT",
        "float": "FLOAT",
        "decimal": "DECIMAL(10,2)",
        "boolean": "BOOLEAN",
        "datetime": "DATETIME(3)",
        "json": "JSON",
        "blob": "BLOB",
    },
    "sqlite": {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "uuid": "TEXT",
        "string_short": "TEXT",
        "string_long": "TEXT",
        "integer": "INTEGER",
        "bigint": "INTEGER",
        "float": "REAL",
        "decimal": "NUMERIC",
        "boolean": "INTEGER",
        "datetime": "TEXT",
        "json": "JSON",
        "blob": "BLOB",
    },
}


class SchemaDesigner:
    """
    Analyzes and recommends optimized database schemas.

    Usage::

        designer = SchemaDesigner()
        recs = designer.design(schema, database_type)
    """

    def design(
        self,
        schema: SchemaDefinition | None,
        database_type: DatabaseType = DatabaseType.postgresql,
    ) -> list[SchemaRecommendation]:
        """
        Analyze schema and produce recommendations.

        Args:
            schema: Current schema definition.
            database_type: Target database type.

        Returns:
            List of SchemaRecommendation objects.
        """
        if not schema or not schema.tables:
            return [SchemaRecommendation(
                table="",
                action="add_table",
                details={"message": "No schema provided — cannot analyze"},
                priority=Severity.low,
                rationale="Provide a schema definition for analysis",
            )]

        recs: list[SchemaRecommendation] = []
        db_key = database_type.value

        for table in schema.tables:
            recs.extend(self._check_table_design(table, db_key))
            recs.extend(self._check_normalization(table))
            recs.extend(self._check_constraints(table))

        return recs

    def _check_table_design(
        self, table: TableDefinition, db_key: str
    ) -> list[SchemaRecommendation]:
        """Check table design for best practices."""
        recs: list[SchemaRecommendation] = []

        # Check for missing primary key.
        if not table.primary_key and not any(c.name == "id" for c in table.columns):
            recs.append(SchemaRecommendation(
                table=table.name,
                action="add_column",
                details={"column": "id", "type": _TYPE_RECOMMENDATIONS.get(db_key, {}).get("id", "SERIAL PRIMARY KEY")},
                priority=Severity.high,
                rationale="Tables should have a primary key for unique row identification and indexing",
            ))

        # Check column types.
        type_map = _TYPE_RECOMMENDATIONS.get(db_key, {})
        for col in table.columns:
            col_type_lower = col.type.lower()
            if "varchar" in col_type_lower and "255" not in col_type_lower:
                try:
                    size = int(col_type_lower.split("(")[1].split(")")[0])
                    if size > 500:
                        recs.append(SchemaRecommendation(
                            table=table.name,
                            action="modify_column",
                            details={"column": col.name, "old_type": col.type, "new_type": "TEXT"},
                            priority=Severity.low,
                            rationale=f"VARCHAR({size}) is large — consider TEXT for variable-length content",
                        ))
                except (IndexError, ValueError):
                    pass

            if "text" in col_type_lower and "json" not in col_type_lower and "timestamp" not in col_type_lower:
                if not any("fulltext" in c.lower() for c in col.constraints):
                    recs.append(SchemaRecommendation(
                        table=table.name,
                        action="add_constraint",
                        details={"column": col.name, "constraint": "consider full-text index if searching"},
                        priority=Severity.low,
                        rationale="TEXT column without index may cause slow searches",
                    ))

        return recs

    def _check_normalization(self, table: TableDefinition) -> list[SchemaRecommendation]:
        """Check for normalization issues."""
        recs: list[SchemaRecommendation] = []

        # Check for repeating groups (multiple columns with similar names).
        col_names = [c.name.lower() for c in table.columns]
        prefixes: dict[str, int] = {}
        for name in col_names:
            parts = name.split("_")
            if len(parts) >= 2:
                prefix = parts[0]
                prefixes[prefix] = prefixes.get(prefix, 0) + 1

        for prefix, count in prefixes.items():
            if count >= 3:
                recs.append(SchemaRecommendation(
                    table=table.name,
                    action="normalize",
                    details={"prefix": prefix, "count": count},
                    priority=Severity.medium,
                    rationale=f"Possible repeating group '{prefix}_*' — consider normalizing to separate table",
                ))

        return recs

    def _check_constraints(self, table: TableDefinition) -> list[SchemaRecommendation]:
        """Check for missing constraints."""
        recs: list[SchemaRecommendation] = []

        for col in table.columns:
            # Check for nullable columns that should be NOT NULL.
            if "not null" not in [c.lower() for c in col.constraints] and col.name in ("email", "username", "id"):
                recs.append(SchemaRecommendation(
                    table=table.name,
                    action="add_constraint",
                    details={"column": col.name, "constraint": "NOT NULL"},
                    priority=Severity.medium,
                    rationale=f"Column '{col.name}' should be NOT NULL for data integrity",
                ))

            # Check for missing UNIQUE on email-like columns.
            if "email" in col.name.lower() and "unique" not in [c.lower() for c in col.constraints]:
                recs.append(SchemaRecommendation(
                    table=table.name,
                    action="add_constraint",
                    details={"column": col.name, "constraint": "UNIQUE"},
                    priority=Severity.high,
                    rationale=f"Column '{col.name}' should be UNIQUE to prevent duplicates",
                ))

        return recs
