"""
RFC-0001 Stable Contract — Pipeline Engine.

Orchestrates cognitive pipeline stages for each pack, emitting events
through the Stable Event Bus and collecting results.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any

from backend.app.core.event_bus import StableEventBus
from backend.app.core.schemas import (
    EmittedEvent,
    EventPriority,
    TaskIntentRequest,
    TaskResult,
    TaskResultMetrics,
    TaskResultPayload,
    TaskStatus,
)
from backend.app.core.schemas import (
    Event as TypedEvent,
)

logger = logging.getLogger(__name__)


class PipelineStage:
    """A single stage in a cognitive pipeline."""

    def __init__(
        self,
        name: str,
        capability: str,
        timeout_ms: int = 30000,
    ):
        self.name = name
        self.capability = capability
        self.timeout_ms = timeout_ms


class PipelineEngine:
    """Orchestrates cognitive pipeline stages (RFC-0001 § Pipeline Engine).

    Each stage maps to a pack capability.  The engine:
      1. Emits a ``pipeline.stage.started`` event
      2. Invokes the stage handler
      3. Emits a ``pipeline.stage.completed`` (or ``.failed``) event
      4. Aggregates results into a TaskResult
    """

    def __init__(self, event_bus: StableEventBus | None = None, use_redis: bool = False):
        self._event_bus = event_bus or StableEventBus(use_redis=use_redis)
        self._stages: dict[str, list[PipelineStage]] = {}
        self._handlers: dict[str, Callable] = {}
        self._execution_history: list[dict[str, Any]] = []

    # -- registration -------------------------------------------------------

    def register_stage_handler(self, capability: str, handler: Callable) -> None:
        """Register a handler for a capability / pipeline stage."""
        self._handlers[capability] = handler

    def define_pipeline(self, pack_id: str, stages: list[PipelineStage]) -> None:
        """Define the cognitive pipeline stages for a pack."""
        self._stages[pack_id] = stages

    def get_pipeline(self, pack_id: str) -> list[PipelineStage]:
        return self._stages.get(pack_id, [])

    # -- execution ----------------------------------------------------------

    async def execute_pipeline(
        self,
        task: TaskIntentRequest,
        pack_id: str,
        stage_results: dict[str, Any] | None = None,
    ) -> TaskResult:
        """Execute the pipeline for *pack_id* against *task*.

        Returns a complete :class:`TaskResult`.
        """
        trace_id = task.metadata.trace_id
        correlation_id = task.metadata.correlation_id
        stages = self._stages.get(pack_id, [])
        stage_results = stage_results or {}
        events_emitted: list[EmittedEvent] = []
        start_time = time.perf_counter()

        events_emitted.append(
            EmittedEvent(
                event_type="pipeline.started",
                payload={"pack_id": pack_id, "stage_count": len(stages)},
            )
        )
        await self._emit(
            "pipeline.started",
            {"pack_id": pack_id, "stage_count": len(stages), "task_id": task.task_id},
            task_id=task.task_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
        )

        failed_stage: str | None = None
        error_message: str | None = None

        for i, stage in enumerate(stages):
            stage_start = time.perf_counter()
            stage_input = {**stage_results, "task": task.model_dump()}

            events_emitted.append(
                EmittedEvent(
                    event_type="pipeline.stage.started",
                    payload={
                        "pack_id": pack_id,
                        "stage_index": i,
                        "stage_name": stage.name,
                        "capability": stage.capability,
                    },
                )
            )
            await self._emit(
                "pipeline.stage.started",
                {
                    "pack_id": pack_id,
                    "stage_index": i,
                    "stage_name": stage.name,
                    "capability": stage.capability,
                },
                task_id=task.task_id,
                trace_id=trace_id,
                correlation_id=correlation_id,
            )

            handler = self._handlers.get(stage.capability)
            if handler is None:
                failed_stage = stage.name
                error_message = f"No handler registered for capability: {stage.capability}"
                events_emitted.append(
                    EmittedEvent(
                        event_type="pipeline.stage.failed",
                        payload={
                            "pack_id": pack_id,
                            "stage_index": i,
                            "stage_name": stage.name,
                            "capability": stage.capability,
                            "error": error_message,
                        },
                    )
                )
                break

            try:
                if _is_async(handler):
                    result = await handler(stage_input)
                else:
                    result = handler(stage_input)

                stage_results[stage.capability] = result
                events_emitted.append(
                    EmittedEvent(
                        event_type="pipeline.stage.completed",
                        payload={
                            "pack_id": pack_id,
                            "stage_index": i,
                            "stage_name": stage.name,
                            "capability": stage.capability,
                            "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
                        },
                    )
                )
            except Exception as exc:
                failed_stage = stage.name
                error_message = str(exc)
                logger.error(f"Pipeline stage '{stage.name}' failed: {exc}")
                events_emitted.append(
                    EmittedEvent(
                        event_type="pipeline.stage.failed",
                        payload={
                            "pack_id": pack_id,
                            "stage_index": i,
                            "stage_name": stage.name,
                            "capability": stage.capability,
                            "error": error_message,
                        },
                    )
                )
                break

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        if failed_stage:
            status: TaskStatus = "failure"
            error_code = "PIPELINE_STAGE_FAILED"
        else:
            status = "success"
            error_code = ""

        events_emitted.append(
            EmittedEvent(
                event_type="pipeline.completed" if not failed_stage else "pipeline.failed",
                payload={
                    "pack_id": pack_id,
                    "task_id": task.task_id,
                    "duration_ms": round(elapsed_ms, 2),
                    "stages_executed": len(events_emitted),
                },
            )
        )
        await self._emit(
            "pipeline.completed" if not failed_stage else "pipeline.failed",
            {
                "pack_id": pack_id,
                "task_id": task.task_id,
                "duration_ms": round(elapsed_ms, 2),
                "stages_executed": len(events_emitted),
            },
            task_id=task.task_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
        )

        result = TaskResult(
            task_id=task.task_id,
            intent=task.intent,
            status=status,
            result=TaskResultPayload(
                output_type="report",
                payload={"stage_results": stage_results, "pack_id": pack_id},
                artifacts=[],
                confidence_score=1.0 if not failed_stage else 0.5,
            ),
            events_emitted=events_emitted,
            metrics=TaskResultMetrics(
                latency_ms=round(elapsed_ms, 2),
                tokens_used=0,
                memory_mb=0.0,
            ),
        )
        if error_code:
            from backend.app.core.schemas import TaskError

            result.error = TaskError(code=error_code, message=error_message or "")

        self._execution_history.append(result.model_dump())
        return result

    # -- internal helpers ---------------------------------------------------

    async def _emit(
        self,
        event_type: str,
        payload: dict[str, Any],
        task_id: str = "",
        trace_id: str | None = None,
        correlation_id: str | None = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> None:
        event = TypedEvent(
            event_type=event_type,
            payload=payload,
            source="pipeline-engine",
            trace_id=trace_id,
            correlation_id=correlation_id,
            priority=priority,
        )
        await self._event_bus.publish(event)

    def get_history(self, task_id: str | None = None) -> list[dict[str, Any]]:
        if task_id:
            return [h for h in self._execution_history if h.get("task_id") == task_id]
        return list(self._execution_history)

    def clear(self) -> None:
        """Reset all registered pipelines, handlers, and history."""
        self._stages.clear()
        self._handlers.clear()
        self._execution_history.clear()


def _is_async(handler: Callable) -> bool:
    import inspect

    return inspect.iscoroutinefunction(handler)


pipeline_engine = PipelineEngine()
