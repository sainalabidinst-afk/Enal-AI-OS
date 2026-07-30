import logging
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from backend.app.core.event_bus import event_bus
from backend.app.core.events import Event
from backend.app.core.state_recovery import state_recovery
from backend.app.core.task_queue import Task, task_queue

logger = logging.getLogger(__name__)


class LongTaskStatus(str, Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class LongTask:
    id: str
    name: str
    workflow: list[dict[str, Any]]
    status: LongTaskStatus = LongTaskStatus.SCHEDULED
    current_step: int = 0
    result: Any = None
    error: str | None = None
    progress: float = 0.0
    started_at: datetime | None = None
    finished_at: datetime | None = None
    checkpoint_data: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class AutonomousLongTask:
    def __init__(self):
        self._tasks: dict[str, LongTask] = {}
        self._handlers: dict[str, Callable[[dict], Awaitable[Any]]] = {}
        event_bus.subscribe("task.completed", self._on_task_completed)
        event_bus.subscribe("task.failed", self._on_task_failed)

    async def submit(self, name: str, workflow: list[dict[str, Any]]) -> str:
        task_id = f"longtask-{uuid.uuid4().hex[:8]}"
        long_task = LongTask(id=task_id, name=name, workflow=workflow)
        self._tasks[task_id] = long_task
        await event_bus.publish(Event(
            event_type="longtask.created",
            payload={"task_id": task_id, "name": name},
            source="longtask-manager",
        ))
        return task_id

    async def start(self, task_id: str):
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Long task not found: {task_id}")
        task.status = LongTaskStatus.RUNNING
        task.started_at = datetime.now(timezone.utc)
        checkpoint = await state_recovery.load(task_id)
        if checkpoint:
            task.current_step = checkpoint.get("step", 0)
            task.checkpoint_data = checkpoint.get("state")
        while task.current_step < len(task.workflow) and task.status == LongTaskStatus.RUNNING:
            step = task.workflow[task.current_step]
            await event_bus.publish(Event(
                event_type="longtask.step.started",
                payload={"task_id": task_id, "step": task.current_step},
                source="longtask-manager",
            ))
            try:
                result = await self._execute_step(step, task.checkpoint_data)
                task.result = result
                task.current_step += 1
                task.progress = (task.current_step / len(task.workflow)) * 100
                await state_recovery.save(task_id, f"step-{task.current_step}", {
                    "step": task.current_step,
                    "state": result,
                    "progress": task.progress,
                })
                await event_bus.publish(Event(
                    event_type="longtask.step.completed",
                    payload={"task_id": task_id, "step": task.current_step - 1, "result": result},
                    source="longtask-manager",
                ))
            except Exception as e:
                task.error = str(e)
                task.status = LongTaskStatus.FAILED
                await event_bus.publish(Event(
                    event_type="longtask.failed",
                    payload={"task_id": task_id, "error": str(e)},
                    source="longtask-manager",
                ))
                break
        if task.status == LongTaskStatus.RUNNING:
            task.status = LongTaskStatus.COMPLETED
            task.progress = 100.0
            await event_bus.publish(Event(
                event_type="longtask.completed",
                payload={"task_id": task_id, "result": task.result},
                source="longtask-manager",
            ))
        task.finished_at = datetime.now(timezone.utc)
        return task

    async def pause(self, task_id: str):
        task = self._tasks.get(task_id)
        if task:
            task.status = LongTaskStatus.PAUSED
            await state_recovery.save(task_id, "paused", {"step": task.current_step, "state": task.checkpoint_data})

    async def resume(self, task_id: str):
        task = self._tasks.get(task_id)
        if task and task.status == LongTaskStatus.PAUSED:
            return await self.start(task_id)
        return None

    async def get_status(self, task_id: str) -> dict[str, Any] | None:
        task = self._tasks.get(task_id)
        if not task:
            return None
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "progress": task.progress,
            "current_step": task.current_step,
            "total_steps": len(task.workflow),
            "error": task.error,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "finished_at": task.finished_at.isoformat() if task.finished_at else None,
        }

    async def _execute_step(self, step: dict[str, Any], context: Any) -> Any:
        step_type = step.get("type", "task")
        if step_type == "task":
            task = Task(name=step.get("name", ""), agent=step.get("agent", "system"), payload=step.get("payload", {}))
            result = await task_queue.execute(task)
            return result.result
        elif step_type == "checkpoint":
            return context
        return None

    async def _on_task_completed(self, event: Event):
        pass

    async def _on_task_failed(self, event: Event):
        pass


long_task_manager = AutonomousLongTask()

