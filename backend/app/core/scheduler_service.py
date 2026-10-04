"""
Scheduler service for cron-like scheduled executions.

Manages scheduled runs of agents, tools, and workflows using APScheduler.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
    """Manage scheduled executions with APScheduler."""

    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()
        self._started = False
        self._jobs: dict[str, ScheduledJob] = {}

    def _ensure_started(self) -> None:
        if not self._started:
            self._scheduler.start()
            self._started = True

    def schedule(self, cron: str, payload: dict[str, Any]) -> ScheduledJob:
        self._ensure_started()
        import uuid

        job_id = str(uuid.uuid4())
        job = ScheduledJob(job_id, cron, payload)
        self._jobs[job_id] = job

        cron_parts = cron.strip().split()
        if len(cron_parts) == 5:
            minute, hour, day, month, day_of_week = cron_parts
            trigger_args = {
                "minute": minute,
                "hour": hour,
                "day": day,
                "month": month,
                "day_of_week": day_of_week,
            }
        else:
            trigger_args = {
                "minute": "*",
                "hour": "*",
                "day": "*",
                "month": "*",
                "day_of_week": "*",
            }

        async def _run_job():
            job.last_run = datetime.now(UTC).isoformat()
            logger.info("Scheduled job %s executed with payload %s", job_id, payload)

        self._scheduler.add_cron_job(
            _run_job,
            id=job_id,
            **trigger_args,
        )
        job.next_run = datetime.now(UTC).isoformat()
        logger.info("Scheduled job %s with cron %s", job_id, cron)
        return job

    def cancel(self, job_id: str) -> bool:
        self._ensure_started()
        if job_id in self._jobs:
            try:
                self._scheduler.remove_job(job_id)
            except Exception:
                pass
            del self._jobs[job_id]
            return True
        return False

    def list_jobs(self) -> list[ScheduledJob]:
        return list(self._jobs.values())


scheduler_service = SchedulerService()
