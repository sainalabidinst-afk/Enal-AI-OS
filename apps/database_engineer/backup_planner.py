"""
Database Engineer — Backup Planner.

Plans backup strategies and recovery procedures based on
RTO (Recovery Time Objective) and RPO (Recovery Point Objective) requirements.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.database_engineer.schemas import (
    DatabaseType,
    BackupPlan,
)

logger = logging.getLogger(__name__)


class BackupPlanner:
    """
    Plans database backup and recovery strategies.

    Usage::

        planner = BackupPlanner()
        plan = planner.plan(database_type, rto_hours, rpo_minutes)
    """

    def plan(
        self,
        database_type: DatabaseType = DatabaseType.postgresql,
        rto_hours: float = 4.0,
        rpo_minutes: int = 60,
    ) -> BackupPlan:
        """
        Plan a backup strategy based on RTO and RPO requirements.

        Args:
            database_type: Target database type.
            rto_hours: Recovery Time Objective in hours.
            rpo_minutes: Recovery Point Objective in minutes.

        Returns:
            BackupPlan with schedule, type, and recovery steps.
        """
        schedule, backup_type = self._determine_schedule(rpo_minutes)
        steps = self._generate_steps(database_type, backup_type, rto_hours)

        return BackupPlan(
            schedule=schedule,
            backup_type=backup_type,
            retention_days=self._determine_retention(rto_hours),
            rto_hours=rto_hours,
            rpo_minutes=rpo_minutes,
            storage_location="encrypted_object_storage",
            encryption_required=True,
            steps=steps,
        )

    def _determine_schedule(self, rpo_minutes: int) -> tuple[str, str]:
        """Determine backup schedule and type from RPO."""
        if rpo_minutes <= 15:
            return "every_15_minutes", "incremental"
        elif rpo_minutes <= 60:
            return "hourly", "incremental"
        elif rpo_minutes <= 720:
            return "daily", "differential"
        else:
            return "daily", "full"

    def _determine_retention(self, rto_hours: float) -> int:
        """Determine retention period from RTO."""
        if rto_hours <= 1:
            return 90  # 3 months
        elif rto_hours <= 4:
            return 30  # 1 month
        elif rto_hours <= 24:
            return 14  # 2 weeks
        else:
            return 7  # 1 week

    def _generate_steps(
        self,
        database_type: DatabaseType,
        backup_type: str,
        rto_hours: float,
    ) -> list[str]:
        """Generate recovery runbook steps."""
        db = database_type.value
        steps = [
            "1. Verify backup integrity: checksum validation",
            f"2. Stop {db} service if running",
            f"3. Restore {backup_type} backup to target directory",
            f"4. Start {db} service and verify connection",
            "5. Run database consistency check (e.g., pg_dump --schema-only)",
            "6. Verify application connectivity and data integrity",
            "7. Update DNS/load balancer if failover occurred",
        ]

        if rto_hours <= 1:
            steps.insert(1, "1.5. Restore from transaction log (WAL/binlog) to minimize data loss")

        return steps
