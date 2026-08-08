import pytest

from backend.app.core.execution_integration import ExecutionScheduler
from backend.app.models.schemas_execution import ExecutionGraph, ExecutionStatus, ExecutionTask


class TestExecutionScheduler:
    async def test_submit_adds_tasks_to_queue(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1")
        task2 = ExecutionTask(id="t2", name="Task 2", dependencies=["t1"])
        graph = ExecutionGraph(tasks={"t1": task1, "t2": task2}, edges=[], entry_point="t1")
        queue = await scheduler.submit("sess-1", graph)
        assert len(queue) == 2

    async def test_next_returns_pending_task_with_met_dependencies(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1")
        task2 = ExecutionTask(id="t2", name="Task 2", dependencies=["t1"])
        graph = ExecutionGraph(tasks={"t1": task1, "t2": task2}, edges=[], entry_point="t1")
        await scheduler.submit("sess-1", graph)
        next_task = await scheduler.next("sess-1")
        assert next_task is not None
        assert next_task.id == "t1"
        assert next_task.status == ExecutionStatus.running

    async def test_next_returns_none_when_no_runnable(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1", dependencies=["t2"])
        graph = ExecutionGraph(tasks={"t1": task1}, edges=[], entry_point="t1")
        await scheduler.submit("sess-1", graph)
        next_task = await scheduler.next("sess-1")
        assert next_task is None

    async def test_complete_marks_task_completed(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1")
        graph = ExecutionGraph(tasks={"t1": task1}, edges=[], entry_point="t1")
        await scheduler.submit("sess-1", graph)
        completed = await scheduler.complete("sess-1", "t1", {"result": "ok"})
        assert completed is not None
        assert completed.status == ExecutionStatus.completed
        assert completed.result == {"result": "ok"}

    async def test_complete_returns_none_for_missing_task(self):
        scheduler = ExecutionScheduler()
        result = await scheduler.complete("sess-1", "missing", {})
        assert result is None

    async def test_fail_marks_task_failed(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1")
        graph = ExecutionGraph(tasks={"t1": task1}, edges=[], entry_point="t1")
        await scheduler.submit("sess-1", graph)
        failed = await scheduler.fail("sess-1", "t1", "error")
        assert failed is not None
        assert failed.status == ExecutionStatus.failed
        assert failed.result == {"error": "error"}

    async def test_fail_returns_none_for_missing_task(self):
        scheduler = ExecutionScheduler()
        result = await scheduler.fail("sess-1", "missing", "error")
        assert result is None

    async def test_dependencies_met_returns_true_when_all_completed(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1", status=ExecutionStatus.completed)
        task2 = ExecutionTask(id="t2", name="Task 2", dependencies=["t1"])
        queue = [task1, task2]
        assert scheduler._dependencies_met(task2, queue) is True

    async def test_dependencies_met_returns_false_when_dependency_not_completed(self):
        scheduler = ExecutionScheduler()
        task1 = ExecutionTask(id="t1", name="Task 1", status=ExecutionStatus.pending)
        task2 = ExecutionTask(id="t2", name="Task 2", dependencies=["t1"])
        queue = [task1, task2]
        assert scheduler._dependencies_met(task2, queue) is False
