import pytest

from backend.app.core.background_tasks import BackgroundTaskManager


class FakeEvent:
    def __init__(self, payload):
        self.payload = payload


class TestBackgroundTaskManager:
    @pytest.fixture
    def manager(self, monkeypatch):
        import backend.app.core.background_tasks as bt_module
        import backend.app.core.event_bus as eb_module

        fake_bus = type("Bus", (), {
            "subscribe": lambda *a, **k: None,
            "publish": lambda *a, **k: None,
        })()
        monkeypatch.setattr(bt_module, "event_bus", fake_bus)
        monkeypatch.setattr(eb_module, "event_bus", fake_bus)

        async def fake_enqueue(self, *args, **kwargs):
            return "task-123"

        async def fake_get_task(self, task_id):
            return None

        fake_queue = type("Queue", (), {
            "enqueue": fake_enqueue,
            "get_task": fake_get_task,
        })()
        monkeypatch.setattr(bt_module, "task_queue", fake_queue)
        return BackgroundTaskManager()

    async def test_submit_returns_task_id(self, manager):
        task_id = await manager.submit("task1", "agent1", {"key": "value"})
        assert task_id == "task-123"

    async def test_get_status_returns_none_when_missing(self, manager):
        status = await manager.get_status("missing")
        assert status is None

    def test_on_complete_registers_callback(self, manager):
        callback = lambda result: None
        manager.on_complete("task-1", callback)
        assert "task-1" in manager._listeners
        assert callback in manager._listeners["task-1"]

    @pytest.mark.asyncio
    async def test_on_task_completed_calls_callbacks(self, manager):
        results = []

        async def callback(result):
            results.append(result)

        manager.on_complete("task-1", callback)
        await manager._on_task_completed(FakeEvent({"task_id": "task-1", "result": "ok"}))
        assert results == ["ok"]
        assert "task-1" not in manager._listeners

    @pytest.mark.asyncio
    async def test_on_task_completed_handles_callback_error(self, manager):
        async def bad_callback(result):
            raise ValueError("fail")

        manager.on_complete("task-1", bad_callback)
        await manager._on_task_completed(FakeEvent({"task_id": "task-1", "result": "ok"}))
        assert "task-1" not in manager._listeners

    @pytest.mark.asyncio
    async def test_on_task_failed_clears_listeners(self, manager):
        manager._listeners["task-1"] = [lambda r: None]
        await manager._on_task_failed(FakeEvent({"task_id": "task-1"}))
        assert "task-1" not in manager._listeners
