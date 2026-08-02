"""
Data Engineer — Schema Evolver.

Detects schema drift between current data and expected schema,
produces migration plans for schema changes.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.data_engineer.schemas import (
    SchemaDriftReport,
    SchemaChange,
    ChangeType,
)

logger = logging.getLogger(__name__)


class SchemaEvolver:
    """
    Detects schema drift and generates migration plans.

    Usage::

        evolver = SchemaEvolver()
        report = evolver.detect_drift(current_data, old_schema, new_schema)
    """

    def detect_drift(
        self,
        data: list[dict[str, Any]],
        old_schema: dict[str, Any] | None,
        new_schema: dict[str, Any] | None,
    ) -> SchemaDriftReport:
        """
        Detect schema drift between old and new schema.

        Args:
            data: Current dataset rows.
            old_schema: Previous schema definition.
            new_schema: Target schema definition.

        Returns:
            SchemaDriftReport with detected changes and migration plan.
        """
        if not old_schema and not new_schema:
            return SchemaDriftReport(detected=False)

        old_cols = set(old_schema.keys()) if old_schema else set()
        new_cols = set(new_schema.keys()) if new_schema else set()
        current_cols = set(data[0].keys()) if data else set()

        changes: list[SchemaChange] = []

        # Detect added columns.
        for col in new_cols - old_cols:
            if col in current_cols:
                changes.append(SchemaChange(
                    column=col,
                    change_type=ChangeType.added,
                    new_type=new_schema.get(col, "unknown"),
                ))

        # Detect removed columns.
        for col in old_cols - new_cols:
            if col in current_cols:
                changes.append(SchemaChange(
                    column=col,
                    change_type=ChangeType.removed,
                    old_type=old_schema.get(col, "unknown"),
                ))

        # Detect type changes.
        for col in old_cols & new_cols:
            if old_schema.get(col) != new_schema.get(col):
                changes.append(SchemaChange(
                    column=col,
                    change_type=ChangeType.type_changed,
                    old_type=old_schema.get(col, "unknown"),
                    new_type=new_schema.get(col, "unknown"),
                ))

        # Detect renamed columns (heuristic: similar values).
        if old_schema and new_schema:
            old_names = set(old_schema.keys())
            new_names = set(new_schema.keys())
            unmatched_new = new_names - old_names
            unmatched_old = old_names - new_names
            for old_name in list(unmatched_old):
                for new_name in list(unmatched_new):
                    if self._is_similar(old_name, new_name):
                        changes.append(SchemaChange(
                            column=new_name,
                            change_type=ChangeType.renamed,
                            old_type=old_schema.get(old_name, "unknown"),
                            new_type=new_schema.get(new_name, "unknown"),
                        ))
                        unmatched_new.discard(new_name)
                        break

        return SchemaDriftReport(
            detected=len(changes) > 0,
            changes=changes,
            migration_required=len(changes) > 0,
        )

    def _is_similar(self, name1: str, name2: str) -> bool:
        """Check if two column names are similar (rename heuristic)."""
        if name1.lower() == name2.lower():
            return True
        # Check for common rename patterns.
        if name1.lower().replace("_", "") == name2.lower().replace("_", ""):
            return True
        if name1.lower().replace("id", "") == name2.lower().replace("uuid", ""):
            return True
        return False
