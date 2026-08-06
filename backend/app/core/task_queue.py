import logging
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from backend.app.core.event_bus import event_bus
from backend.app.core.events import Event

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    agent: str = "system"
    status: TaskStatus = TaskStatus.PENDING
    payload: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: str | None = None
    depends_on: list[str] = field(default_factory=list)
    priority: int = 0
    retries: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now(UTC))
    started_at: datetime | None = None
    finished_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskQueue:
    def __init__(self):
        self._tasks: dict[str, Task] = {}
        self._handlers: dict[str, Callable[[Task], Awaitable[None]]] = {}
        event_bus.subscribe("task.created", self._on_task_created)
        event_bus.subscribe("task.completed", self._on_task_completed)
        event_bus.subscribe("task.failed", self._on_task_failed)

    async def _on_task_created(self, event: Event):
        task_data = event.payload.get("task", {})
        task = Task(**task_data)
        self._tasks[task.id] = task
        logger.info(f"Task created: {task.id} ({task.name})")

    async def _on_task_completed(self, event: Event):
        task_id = event.payload.get("task_id")
        if task_id in self._tasks:
            self._tasks[task_id].status = TaskStatus.COMPLETED
            self._tasks[task_id].result = event.payload.get("result")
            self._tasks[task_id].finished_at = datetime.now(UTC)

    async def _on_task_failed(self, event: Event):
        task_id = event.payload.get("task_id")
        if task_id in self._tasks:
            task = self._tasks[task_id]
            task.error = event.payload.get("error")
            task.retries += 1
            if task.retries < task.max_retries:
                task.status = TaskStatus.QUEUED
                await self.enqueue(task)
            else:
                task.status = TaskStatus.FAILED
                task.finished_at = datetime.now(UTC)

    async def enqueue(self, task: Task) -> str:
        task.status = TaskStatus.QUEUED
        self._tasks[task.id] = task
        await event_bus.publish(Event(
            event_type="task.created",
            payload={"task": self._serialize(task)},
            source="task-queue",
        ))
        return task.id

    async def execute(self, task: Task) -> Task:
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now(UTC)
        handler = self._handlers.get(task.agent)
        if not handler:
            raise ValueError(f"No handler for agent: {task.agent}")
        try:
            task.result = await handler(task)  # type: ignore[func-returns-value]
            task.status = TaskStatus.COMPLETED
            await event_bus.publish(Event(
                event_type="task.completed",
                payload={"task_id": task.id, "result": task.result},
                source="task-queue",
            ))
        except Exception as e:
            task.error = str(e)
            await event_bus.publish(Event(
                event_type="task.failed",
                payload={"task_id": task.id, "error": str(e)},
                source="task-queue",
            ))
        task.finished_at = datetime.now(UTC)
        return task

    def register_handler(self, agent: str, handler: Callable[[Task], Awaitable[None]]) -> None:
        self._handlers[agent] = handler

    async def get_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    async def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks

    def _serialize(self, task: Task) -> dict[str, Any]:
        return {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "agent": task.agent,
            "status": task.status.value,
            "payload": task.payload,
            "depends_on": task.depends_on,
            "priority": task.priority,
            "retries": task.retries,
            "max_retries": task.max_retries,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "finished_at": task.finished_at.isoformat() if task.finished_at else None,
            "metadata": task.metadata,
        }


task_queue = TaskQueue()

