import logging

import pytest

from backend.app.core.task_queue import Task, TaskQueue, TaskStatus
from backend.app.core.events import Event


class FakeEventBus:
    def __init__(self):
        self.subscribed = {}
        self.published = []

    def subscribe(self, event_type, callback):
        self.subscribed.setdefault(event_type, []).append(callback)

    async def publish(self, event):
        self.published.append(event)


class FakeHandler:
    def __init__(self, result=None, raise_error=None):
        self.result = result
        self.raise_error = raise_error

    async def __call__(self, task):
        if self.raise_error:
            raise self.raise_error
        return self.result


class TestTaskStatus:
    def test_values(self):
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.QUEUED == "queued"
        assert TaskStatus.RUNNING == "running"
        assert TaskStatus.COMPLETED == "completed"
        assert TaskStatus.FAILED == "failed"
        assert TaskStatus.CANCELLED == "cancelled"


class TestTask:
    def test_defaults(self):
        task = Task()
        assert task.id is not None
        assert task.name == ""
        assert task.status == TaskStatus.PENDING
        assert task.priority == 0
        assert task.max_retries == 3
        assert task.retries == 0

    def test_custom_values(self):
        task = Task(id="t1", name="Test", agent="agent-a", priority=5, max_retries=5)
        assert task.id == "t1"
        assert task.name == "Test"
        assert task.agent == "agent-a"
        assert task.priority == 5
        assert task.max_retries == 5


class TestTaskQueue:
    @pytest.fixture
    def queue(self, monkeypatch):
        import backend.app.core.task_queue as tq_module
        fake_bus = FakeEventBus()
        monkeypatch.setattr(tq_module, "event_bus", fake_bus)
        return TaskQueue(), fake_bus

    async def test_enqueue_publishes_event(self, queue):
        q, bus = queue
        task = Task(name="task1", agent="agent-a")
        task_id = await q.enqueue(task)
        assert task_id == task.id
        assert task.status == TaskStatus.QUEUED
        assert len(bus.published) == 1
        assert bus.published[0].event_type == "task.created"

    async def test_execute_success_publishes_completed(self, queue):
        q, bus = queue
        task = Task(name="task1", agent="agent-a")
        await q.enqueue(task)
        q.register_handler("agent-a", FakeHandler(result="ok"))
        result = await q.execute(task)
        assert result.status == TaskStatus.COMPLETED
        assert result.result == "ok"
        assert len([e for e in bus.published if e.event_type == "task.completed"]) == 1

    async def test_execute_failure_publishes_failed(self, queue):
        q, bus = queue
        task = Task(name="task1", agent="agent-a")
        await q.enqueue(task)
        q.register_handler("agent-a", FakeHandler(raise_error=RuntimeError("boom")))
        result = await q.execute(task)
        assert result.error == "boom"
        assert len([e for e in bus.published if e.event_type == "task.failed"]) == 1

    async def test_execute_no_handler_raises(self, queue):
        q, _ = queue
        task = Task(name="task1", agent="unknown")
        with pytest.raises(ValueError):
            await q.execute(task)

    async def test_get_task_returns_none_for_missing(self, queue):
        q, _ = queue
        assert await q.get_task("missing") is None

    async def test_list_tasks_empty(self, queue):
        q, _ = queue
        assert await q.list_tasks() == []

    async def test_list_tasks_filters_by_status(self, queue):
        q, _ = queue
        t1 = Task(name="t1", agent="a")
        t2 = Task(name="t2", agent="a")
        await q.enqueue(t1)
        await q.enqueue(t2)
        t1.status = TaskStatus.COMPLETED
        tasks = await q.list_tasks(status=TaskStatus.COMPLETED)
        assert len(tasks) == 1
        assert tasks[0].id == t1.id

    async def test_on_task_created_adds_task(self, queue):
        q, _ = queue
        event = Event(event_type="task.created", payload={"task": q._serialize(Task(name="t1", agent="a"))}, source="test")
        await q._on_task_created(event)
        assert len(q._tasks) == 1

    async def test_on_task_completed_updates_task(self, queue):
        q, _ = queue
        task = Task(name="t1", agent="a")
        await q.enqueue(task)
        event = Event(event_type="task.completed", payload={"task_id": task.id, "result": "ok"}, source="test")
        await q._on_task_completed(event)
        assert q._tasks[task.id].status == TaskStatus.COMPLETED
        assert q._tasks[task.id].result == "ok"

    async def test_on_task_failed_retries_and_requeues(self, queue):
        q, _ = queue
        task = Task(name="t1", agent="a", max_retries=2)
        await q.enqueue(task)
        event = Event(event_type="task.failed", payload={"task_id": task.id, "error": "boom"}, source="test")
        await q._on_task_failed(event)
        assert q._tasks[task.id].retries == 1
        assert q._tasks[task.id].status == TaskStatus.QUEUED

    async def test_on_task_failed_exhausts_retries(self, queue):
        q, _ = queue
        task = Task(name="t1", agent="a", max_retries=0)
        await q.enqueue(task)
        event = Event(event_type="task.failed", payload={"task_id": task.id, "error": "boom"}, source="test")
        await q._on_task_failed(event)
        assert q._tasks[task.id].retries == 1
        assert q._tasks[task.id].status == TaskStatus.FAILED
        assert q._tasks[task.id].finished_at is not None

    def test_serialize_returns_dict(self, queue):
        q, _ = queue
        task = Task(name="t1", agent="a")
        data = q._serialize(task)
        assert data["id"] == task.id
        assert data["name"] == "t1"
        assert data["status"] == TaskStatus.PENDING
