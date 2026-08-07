import pytest

from backend.app.core.background_tasks import BackgroundTaskManager


class TestBackgroundTaskManager:
    @pytest.mark.asyncio
    async def test_submit_returns_task_id(self):
        try:
            import redis
            redis_client = redis.Redis(host="localhost", port=6379)
            redis_client.ping()
        except Exception:
            pytest.skip("Redis not available in test environment")

        manager = BackgroundTaskManager()
        task_id = await manager.submit("scan", "network", {"target": "10.0.0.1"})
        assert isinstance(task_id, str)
        assert len(task_id) > 0

    @pytest.mark.asyncio
    async def test_get_status_returns_none_for_unknown_task(self):
        manager = BackgroundTaskManager()
        status = await manager.get_status("nonexistent-task-id")
        assert status is None

    @pytest.mark.asyncio
    async def test_on_complete_registers_callback(self):
        manager = BackgroundTaskManager()
        manager.on_complete("task-1", lambda result: None)
        assert "task-1" in manager._listeners
        assert len(manager._listeners["task-1"]) == 1
