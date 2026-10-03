"""
Bulk, Scheduled, and Evaluation API endpoints.

Provides endpoints for bulk execution, scheduling, webhooks, and evaluations.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from backend.app.core.bulk_executor import bulk_executor
from backend.app.core.evaluator_engine import evaluator_engine
from backend.app.core.scheduled_evaluator import scheduled_evaluator
from backend.app.core.scheduler_service import scheduler_service
from backend.app.core.webhook_service import webhook_service

router = APIRouter()
logger = logging.getLogger(__name__)


class BulkRunRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    tasks: list[dict[str, Any]] = []
    max_concurrency: int = 10


class ScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    cron: str = ""
    payload: dict[str, Any] = {}


class EvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    output: str = ""
    criteria: dict[str, Any] = {}


class WebhookRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str = ""
    payload: dict[str, Any] = {}


@router.post("/bulk/run")
async def run_bulk(request: BulkRunRequest):
    started = time.perf_counter()
    try:

        async def executor(task: dict[str, Any]) -> dict[str, Any]:
            return {"task_id": task.get("id"), "result": "simulated"}

        results = await bulk_executor.run_batch(request.tasks, executor)
        logger.info(
            "Bulk run completed %d tasks in %.2fms",
            len(request.tasks),
            (time.perf_counter() - started) * 1000,
        )
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error("Bulk run failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/schedule")
async def create_schedule(request: ScheduleRequest):
    started = time.perf_counter()
    try:
        job = scheduler_service.schedule(request.cron, request.payload)
        logger.info(
            "Created schedule %s in %.2fms",
            job.job_id,
            (time.perf_counter() - started) * 1000,
        )
        return {
            "job_id": job.job_id,
            "cron": job.cron,
            "next_run": job.next_run,
            "created_at": job.created_at,
        }
    except Exception as e:
        logger.error("Failed to create schedule: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/schedule")
async def list_schedules():
    try:
        jobs = scheduler_service.list_jobs()
        return [
            {
                "job_id": job.job_id,
                "cron": job.cron,
                "next_run": job.next_run,
                "last_run": job.last_run,
            }
            for job in jobs
        ]
    except Exception as e:
        logger.error("Failed to list schedules: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/schedule/{job_id}")
async def delete_schedule(job_id: str):
    deleted = scheduler_service.cancel(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Deleted"}


@router.post("/webhooks/send")
async def send_webhook(request: WebhookRequest):
    started = time.perf_counter()
    try:
        result = await webhook_service.send(request.url, request.payload)
        logger.info(
            "Sent webhook to %s in %.2fms",
            request.url,
            (time.perf_counter() - started) * 1000,
        )
        return result
    except Exception as e:
        logger.error("Failed to send webhook: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/evaluate")
async def evaluate_output(request: EvaluationRequest):
    started = time.perf_counter()
    try:
        result = await evaluator_engine.evaluate(request.output, request.criteria)
        logger.info("Evaluated output in %.2fms", (time.perf_counter() - started) * 1000)
        return result
    except Exception as e:
        logger.error("Evaluation failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/evaluate/results")
async def get_evaluation_results():
    try:
        results = scheduled_evaluator.get_results()
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error("Failed to get evaluation results: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
