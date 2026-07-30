import asyncio
from datetime import UTC, datetime
from typing import Any

from backend.app.core.artifact_service import artifact_service
from backend.app.core.execution_session import execution_session_manager
from backend.app.core.notification_service import notification_service
from backend.app.core.workspace_service import workspace_service
from backend.app.models.schemas_execution import (
    ExecutionGraph,
    ExecutionSession,
    ExecutionStatus,
    ExecutionTask,
)


class ExecutionScheduler:
    def __init__(self) -> None:
        self._queues: dict[str, list[ExecutionTask]] = {}
        self._lock = asyncio.Lock()

    async def submit(self, session_id: str, graph: ExecutionGraph) -> list[ExecutionTask]:
        async with self._lock:
            queue: list[ExecutionTask] = []
            for task_id, task in graph.tasks.items():
                queue.append(task)
            self._queues[session_id] = queue
            return queue

    async def next(self, session_id: str) -> ExecutionTask | None:
        queue = self._queues.get(session_id, [])
        for task in queue:
            if task.status == ExecutionStatus.pending and self._dependencies_met(task, queue):
                task.status = ExecutionStatus.running
                task.started_at = datetime.now(UTC)
                return task
        return None

    async def complete(self, session_id: str, task_id: str, result: dict[str, Any]) -> ExecutionTask | None:
        queue = self._queues.get(session_id, [])
        for task in queue:
            if task.id == task_id:
                task.status = ExecutionStatus.completed
                task.completed_at = datetime.now(UTC)
                task.result = result
                return task
        return None

    async def fail(self, session_id: str, task_id: str, error: str) -> ExecutionTask | None:
        queue = self._queues.get(session_id, [])
        for task in queue:
            if task.id == task_id:
                task.status = ExecutionStatus.failed
                task.result = {"error": error}
                return task
        return None

    def _dependencies_met(self, task: ExecutionTask, queue: list[ExecutionTask]) -> bool:
        task_map = {t.id: t for t in queue}
        for dep_id in task.dependencies:
            dep = task_map.get(dep_id)
            if not dep or dep.status != ExecutionStatus.completed:
                return False
        return True


class ExecutionIntegration:
    def __init__(self) -> None:
        self.scheduler = ExecutionScheduler()
        self._progress_callbacks: list[Any] = []

    def on_progress(self, callback: Any) -> None:
        self._progress_callbacks.append(callback)

    async def _notify_progress(self, event: dict[str, Any]) -> None:
        for callback in self._progress_callbacks:
            try:
                await callback(event)
            except Exception:
                pass

    async def execute(self, goal: str, workspace_id: str, conversation_id: str | None = None) -> ExecutionSession:
        session = await execution_session_manager.create_session(
            goal=goal,
            conversation_id=conversation_id,
            workspace_id=workspace_id,
        )
        await execution_session_manager.add_log(session.id, "Execution session created", level="info")

        ws = await workspace_service.get_workspace(workspace_id)
        if not ws:
            raise ValueError(f"Workspace {workspace_id} not found")

        async def _notify(event: dict[str, Any]) -> None:
            await self._notify_progress(event)
            recipient = conversation_id or session.id
            await notification_service.send(
                recipient=recipient,
                message=event.get("message", event.get("status", "progress")),
                channel="websocket",
                metadata={"session_id": session.id, "event": event},
            )

        self._progress_callbacks.append(_notify)
        try:
            return await self._run(goal, workspace_id, conversation_id, session, ws)
        finally:
            self._progress_callbacks = [cb for cb in self._progress_callbacks if cb != _notify]

    async def _run(self, goal: str, workspace_id: str, conversation_id: str | None, session: ExecutionSession, ws: Any) -> ExecutionSession:

        graph = ExecutionGraph(
            tasks={
                "understand": ExecutionTask(id="understand", name="Goal Understanding"),
                "plan": ExecutionTask(id="plan", name="Execution Planning", dependencies=["understand"]),
                "execute": ExecutionTask(id="execute", name="Execute Tasks", dependencies=["plan"]),
                "verify": ExecutionTask(id="verify", name="Verification", dependencies=["execute"]),
            },
            edges=[
                {"from": "understand", "to": "plan"},
                {"from": "plan", "to": "execute"},
                {"from": "execute", "to": "verify"},
            ],
            entry_point="understand",
        )
        session.graph = graph.model_dump()
        await execution_session_manager.add_log(session.id, "Execution graph created", metadata={"tasks": list(graph.tasks.keys())})

        await execution_session_manager.update_status(session.id, ExecutionStatus.running)
        await self._notify_progress({"type": "status", "session_id": session.id, "status": "running", "message": "Menjalankan eksekusi..."})

        queue = await self.scheduler.submit(session.id, graph)
        results: dict[str, Any] = {}

        for task in queue:
            await execution_session_manager.update_progress(session.id, (list(graph.tasks.keys()).index(task.id) / len(queue)) * 100.0)
            await self._notify_progress({
                "type": "task",
                "session_id": session.id,
                "task_id": task.id,
                "name": task.name,
                "status": "running",
            })

            try:
                result = await self._run_task(session.id, task, ws)
                await self.scheduler.complete(session.id, task.id, result)
                results[task.id] = result
                await execution_session_manager.add_log(session.id, f"Task completed: {task.name}", metadata={"task_id": task.id})
                await self._notify_progress({
                    "type": "task",
                    "session_id": session.id,
                    "task_id": task.id,
                    "name": task.name,
                    "status": "completed",
                })
            except Exception as exc:
                await self.scheduler.fail(session.id, task.id, str(exc))
                await execution_session_manager.update_status(session.id, ExecutionStatus.failed, error=str(exc))
                await self._notify_progress({
                    "type": "error",
                    "session_id": session.id,
                    "task_id": task.id,
                    "message": str(exc),
                })
                raise

        result_artifact = await artifact_service.create_artifact(
            workspace_id=workspace_id,
            name=f"Execution Result - {goal[:50]}",
            artifact_type="execution_result",
            content=str(results),
            metadata={"execution_id": session.id, "goal": goal},
        )
        session.artifacts.append(result_artifact.id)
        await execution_session_manager.add_log(session.id, f"Artifact created: {result_artifact.name}", metadata={"artifact_id": result_artifact.id})

        await execution_session_manager.update_status(session.id, ExecutionStatus.completed)
        await execution_session_manager.update_progress(session.id, 100.0)
        await self._notify_progress({"type": "complete", "session_id": session.id, "message": "Eksekusi selesai"})

        return session

    async def _run_task(self, session_id: str, task: ExecutionTask, workspace: Any) -> dict[str, Any]:
        await asyncio.sleep(0.1)
        return {"task_id": task.id, "name": task.name, "status": "completed", "result": f"{task.name} completed"}


execution_integration = ExecutionIntegration()

