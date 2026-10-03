"""
Scheduler service for cron-like scheduled executions.

Manages scheduled runs of agents, tools, and workflows.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class ScheduledJob:
    def __init__(self, job_id: str, cron: str, payload: dict[str, Any]) -> None:
        self.job_id = job_id
        self.cron = cron
        self.payload = payload
        self.created_at = datetime.now(UTC).isoformat()
        self.next_run: str | None = None
        self.last_run: str | None = None


class SchedulerService:
    """Manage scheduled executions."""

    def __init__(self) -> None:
        self._jobs: dict[str, ScheduledJob] = {}

    def schedule(self, cron: str, payload: dict[str, Any]) -> ScheduledJob:
        job_id = str(id(payload))
        job = ScheduledJob(job_id, cron, payload)
        self._jobs[job_id] = job
        logger.info("Scheduled job %s with cron %s", job_id, cron)
        return job

    def cancel(self, job_id: str) -> bool:
        if job_id in self._jobs:
            del self._jobs[job_id]
            return True
        return False

    def list_jobs(self) -> list[ScheduledJob]:
        return list(self._jobs.values())


scheduler_service = SchedulerService()
