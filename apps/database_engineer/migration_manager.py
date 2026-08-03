"""
Database Engineer — Migration Manager.

Generates forward and rollback migration scripts with
conflict detection and version tracking.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.database_engineer.schemas import (
    MigrationPlan,
    MigrationStep,
    SchemaDefinition,
    TableDefinition,
)

logger = logging.getLogger(__name__)


class MigrationManager:
    """
    Plans and generates database migration scripts.

    Usage::

        manager = MigrationManager()
        plan = manager.plan(from_version, to_version, schema)
    """

    def plan(
        self,
        from_version: str,
        to_version: str,
        schema: SchemaDefinition | None = None,
    ) -> MigrationPlan:
        """
        Generate a migration plan between schema versions.

        Args:
            from_version: Current schema version.
            to_version: Target schema version.
            schema: Target schema definition.

        Returns:
            MigrationPlan with steps and rollback SQL.
        """
        steps: list[MigrationStep] = []
        conflicts: list[str] = []

        if not schema or not schema.tables:
            return MigrationPlan(
                from_version=from_version,
                to_version=to_version,
                steps=[MigrationStep(
                    step_number=1,
                    action="COMMENT",
                    sql="-- No schema changes detected",
                    rollback_sql="-- No rollback needed",
                    description="Schema unchanged between versions",
                )],
            )

        # Generate migration steps from schema.
        for i, table in enumerate(schema.tables, 1):
            col_defs = []
            for col in table.columns:
                constraints = " ".join(col.constraints)
                col_def = f"{col.name} {col.type} {constraints}".strip()
                col_defs.append(col_def)

            if table.primary_key:
                pk = f", PRIMARY KEY ({', '.join(table.primary_key)})"
                col_defs.append(pk)

            for fk in table.foreign_keys:
                col_defs.append(
                    f"FOREIGN KEY ({fk.column}) REFERENCES {fk.references}({fk.references_column})"
                )

            sql = f"CREATE TABLE IF NOT EXISTS {table.name} ({', '.join(col_defs)});"
            rollback = f"DROP TABLE IF EXISTS {table.name};"

            steps.append(MigrationStep(
                step_number=i,
                action="CREATE",
                sql=sql,
                rollback_sql=rollback,
                description=f"Create table {table.name}",
            ))

        # Detect potential conflicts.
        if from_version == to_version:
            conflicts.append("Source and target versions are identical — no migration needed")

        return MigrationPlan(
            from_version=from_version,
            to_version=to_version,
            steps=steps,
            conflicts=conflicts,
            rollback_available=True,
        )

    def generate_rollback(self, plan: MigrationPlan) -> list[str]:
        """
        Generate rollback scripts from a migration plan.

        Args:
            plan: MigrationPlan to reverse.

        Returns:
            List of rollback SQL statements.
        """
        rollbacks: list[str] = []
        for step in reversed(plan.steps):
            if step.rollback_sql:
                rollbacks.append(f"-- Rollback step {step.step_number}: {step.description}")
                rollbacks.append(step.rollback_sql)
        return rollbacks

    def detect_conflicts(
        self,
        plan_a: MigrationPlan,
        plan_b: MigrationPlan,
    ) -> list[str]:
        """
        Detect conflicts between two migration plans.

        Args:
            plan_a: First migration plan.
            plan_b: Second migration plan.

        Returns:
            List of conflict descriptions.
        """
        conflicts: list[str] = []

        tables_a = self._extract_tables(plan_a)
        tables_b = self._extract_tables(plan_b)

        for table in tables_a & tables_b:
            if self._has_conflicting_changes(plan_a, plan_b, table):
                conflicts.append(f"Table '{table}' modified in both migrations — conflict")

        return conflicts

    def _extract_tables(self, plan: MigrationPlan) -> set[str]:
        """Extract table names from migration steps."""
        tables: set[str] = set()
        for step in plan.steps:
            match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', step.sql, re.IGNORECASE)
            if match:
                tables.add(match.group(1))
        return tables

    def _has_conflicting_changes(self, plan_a: MigrationPlan, plan_b: MigrationPlan, table: str) -> bool:
        """Check if two plans have conflicting changes on the same table."""
        steps_a = [s for s in plan_a.steps if table in s.sql]
        steps_b = [s for s in plan_b.steps if table in s.sql]
        return len(steps_a) > 0 and len(steps_b) > 0
