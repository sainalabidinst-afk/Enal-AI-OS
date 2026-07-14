"""
Execution Runtime
================

Executes an ExecutionPlan against a worker pool / agent pool.
Handles retry, timeout, cancellation, result aggregation, and emits
progress events.

This is the runtime bridge between ExecutionPlanner and actual
micro-agent execution.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Awaitable, Callable

from apps.organization.execution_planner import ExecutionPlan, ExecutionStage
from apps.organization.task_planner import SubTask

logger = logging.getLogger(__name__)


class SubtaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


@dataclass
class SubtaskResult:
    subtask_id: str
    status: SubtaskStatus
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    attempts: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float:
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return 0.0


@dataclass
class ExecutionContext:
    execution_id: str
    plan: ExecutionPlan
    worker: Callable[[SubTask, dict[str, Any]], Awaitable[dict[str, Any]]]
    concurrency: int = 4
    retry_limit: int = 2
    retry_delay_seconds: float = 1.0
    timeout_seconds: float = 60.0
    metadata: dict[str, Any] = field(default_factory=dict)


class ExecutionRuntime:
    """Runs ExecutionPlan stages against a worker pool."""

    def __init__(self) -> None:
        self._history: dict[str, list[SubtaskResult]] = {}

    async def execute(self, context: ExecutionContext) -> list[SubtaskResult]:
        execution_id = context.execution_id
        results: list[SubtaskResult] = []
        self._history[execution_id] = []

        for stage in context.plan.stages:
            stage_results = await self._run_stage(stage, context)
            results.extend(stage_results)
            self._history[execution_id].extend(stage_results)
            failed = [r for r in stage_results if r.status == SubtaskStatus.FAILED]
            if stage.mode == "serial" and failed:
                break
        return results

    async def _run_stage(self, stage: ExecutionStage, context: ExecutionContext) -> list[SubtaskResult]:
        if stage.mode == "parallel":
            tasks = [self._run_subtask(subtask, context) for subtask in stage.subtasks]
            return list(await asyncio.gather(*tasks, return_exceptions=False))
        results: list[SubtaskResult] = []
        for subtask in stage.subtasks:
            result = await self._run_subtask(subtask, context)
            results.append(result)
            if result.status == SubtaskStatus.FAILED:
                break
        return results

    async def _run_subtask(self, subtask: SubTask, context: ExecutionContext) -> SubtaskResult:
        attempt = 0
        result = SubtaskResult(subtask_id=subtask.subtask_id, status=SubtaskStatus.PENDING)
        while attempt <= context.retry_limit:
            attempt += 1
            result.attempts = attempt
            result.status = SubtaskStatus.RUNNING
            result.started_at = datetime.utcnow()
            logger.info("Subtask started: %s attempt=%d", subtask.subtask_id, attempt)
            try:
                task_context = {
                    "subtask": {
                        "id": subtask.subtask_id,
                        "name": subtask.name,
                        "required_skills": subtask.required_skills,
                        "produces_artifact": subtask.produces_artifact,
                        "priority": subtask.priority,
                        "can_parallelize": subtask.can_parallelize,
                        "depends_on": subtask.depends_on,
                    }
                }
                worker_output = await asyncio.wait_for(
                    context.worker(subtask, task_context),
                    timeout=context.timeout_seconds,
                )
                result.status = SubtaskStatus.COMPLETED
                result.result = worker_output
                result.finished_at = datetime.utcnow()
                logger.info("Subtask completed: %s duration=%.2fs", subtask.subtask_id, result.duration_seconds)
                return result
            except asyncio.TimeoutError:
                logger.warning("Subtask timeout: %s attempt=%d", subtask.subtask_id, attempt)
                result.error = "timeout"
            except Exception as exc:
                logger.error("Subtask failed: %s attempt=%d error=%s", subtask.subtask_id, attempt, exc)
                result.error = str(exc)
            result.status = SubtaskStatus.RETRYING if attempt < context.retry_limit else SubtaskStatus.FAILED
            result.finished_at = datetime.utcnow()
            if result.status == SubtaskStatus.RETRYING:
                await asyncio.sleep(context.retry_delay_seconds)
        return result

    def get_execution_history(self, execution_id: str) -> list[SubtaskResult]:
        return list(self._history.get(execution_id, []))


execution_runtime = ExecutionRuntime()
