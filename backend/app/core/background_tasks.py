import logging
from collections.abc import Callable
from typing import Any

from backend.app.core.event_bus import event_bus
from backend.app.core.task_queue import Task, TaskStatus, task_queue

logger = logging.getLogger(__name__)


class BackgroundTaskManager:
    def __init__(self):
        event_bus.subscribe("task.completed", self._on_task_completed)
        event_bus.subscribe("task.failed", self._on_task_failed)
        self._listeners: dict[str, list[Callable]] = {}

    async def submit(self, name: str, agent: str, payload: dict[str, Any]) -> str:
        task = Task(name=name, agent=agent, payload=payload)
        task_id = await task_queue.enqueue(task)
        return task_id

    async def get_status(self, task_id: str) -> dict[str, Any] | None:
        task = await task_queue.get_task(task_id)
        if not task:
            return None
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "progress": 0 if task.status == TaskStatus.RUNNING else 100,
            "error": task.error,
            "result": task.result,
            "created_at": task.created_at.isoformat(),
            "finished_at": task.finished_at.isoformat() if task.finished_at else None,
        }

    def on_complete(self, task_id: str, callback):
        self._listeners.setdefault(task_id, []).append(callback)

    async def _on_task_completed(self, event):
        task_id = event.payload.get("task_id")
        callbacks = self._listeners.get(task_id, [])
        for cb in callbacks:
            try:
                await cb(event.payload.get("result"))
            except Exception as e:
                logger.error(f"Background task callback error: {e}")
        self._listeners.pop(task_id, None)

    async def _on_task_failed(self, event):
        task_id = event.payload.get("task_id")
        self._listeners.pop(task_id, None)


background_task_manager = BackgroundTaskManager()
