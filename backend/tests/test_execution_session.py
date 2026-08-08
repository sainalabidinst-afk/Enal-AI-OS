import pytest

from backend.app.core.execution_session import ExecutionSessionManager
from backend.app.models.schemas_execution import ExecutionStatus


class TestExecutionSessionManager:
    @pytest.mark.asyncio
    async def test_create_session(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("goal1", conversation_id="conv1", workspace_id="ws1")
        assert session.goal == "goal1"
        assert session.conversation_id == "conv1"
        assert session.workspace_id == "ws1"
        assert session.id is not None

    @pytest.mark.asyncio
    async def test_get_session_returns_none_for_missing(self):
        mgr = ExecutionSessionManager()
        assert await mgr.get_session("missing") is None

    @pytest.mark.asyncio
    async def test_list_sessions_empty(self):
        mgr = ExecutionSessionManager()
        assert await mgr.list_sessions() == []

    @pytest.mark.asyncio
    async def test_list_sessions_filters_by_workspace(self):
        mgr = ExecutionSessionManager()
        s1 = await mgr.create_session("g1", workspace_id="ws1")
        s2 = await mgr.create_session("g2", workspace_id="ws2")
        sessions = await mgr.list_sessions(workspace_id="ws1")
        assert len(sessions) == 1
        assert sessions[0].id == s1.id

    @pytest.mark.asyncio
    async def test_update_status_sets_completed(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        updated = await mgr.update_status(session.id, ExecutionStatus.completed)
        assert updated.status == ExecutionStatus.completed
        assert updated.progress == 100.0
        assert updated.completed_at is not None

    @pytest.mark.asyncio
    async def test_update_status_with_error(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        updated = await mgr.update_status(session.id, ExecutionStatus.failed, error="boom")
        assert updated.status == ExecutionStatus.failed
        assert updated.error == "boom"

    @pytest.mark.asyncio
    async def test_update_status_returns_none_for_missing(self):
        mgr = ExecutionSessionManager()
        assert await mgr.update_status("missing", ExecutionStatus.completed) is None

    @pytest.mark.asyncio
    async def test_update_progress_clamps_values(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        updated = await mgr.update_progress(session.id, 150.0)
        assert updated.progress == 100.0
        updated2 = await mgr.update_progress(session.id, -10.0)
        assert updated2.progress == 0.0

    @pytest.mark.asyncio
    async def test_update_progress_sets_eta(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        updated = await mgr.update_progress(session.id, 50.0, eta_seconds=60)
        assert updated.eta_seconds == 60

    @pytest.mark.asyncio
    async def test_add_phase_appends_phase(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        phase = await mgr.add_phase(session.id, "Phase 1")
        assert phase["name"] == "Phase 1"
        assert phase["status"] == ExecutionStatus.pending

    @pytest.mark.asyncio
    async def test_add_phase_returns_none_for_missing_session(self):
        mgr = ExecutionSessionManager()
        assert await mgr.add_phase("missing", "Phase 1") is None

    @pytest.mark.asyncio
    async def test_update_phase_returns_none_for_missing_phase(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        result = await mgr.update_phase(session.id, "missing-phase", ExecutionStatus.running)
        assert result is None

    @pytest.mark.asyncio
    async def test_add_log_appends_entry(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        entry = await mgr.add_log(session.id, "test message", level="warning")
        assert entry["message"] == "test message"
        assert entry["level"] == "warning"
        assert "timestamp" in entry

    @pytest.mark.asyncio
    async def test_add_log_returns_none_for_missing_session(self):
        mgr = ExecutionSessionManager()
        assert await mgr.add_log("missing", "msg") is None

    @pytest.mark.asyncio
    async def test_add_artifact_creates_artifact(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        artifact = await mgr.add_artifact(session.id, "art1", "file", content="hello")
        assert artifact.name == "art1"
        assert artifact.type == "file"
        assert artifact.content == "hello"

    @pytest.mark.asyncio
    async def test_add_artifact_returns_none_for_missing_session(self):
        mgr = ExecutionSessionManager()
        assert await mgr.add_artifact("missing", "art1", "file") is None

    @pytest.mark.asyncio
    async def test_get_execution_artifact(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        artifact = await mgr.add_artifact(session.id, "art1", "file")
        fetched = await mgr.get_execution_artifact(artifact.id)
        assert fetched.id == artifact.id

    @pytest.mark.asyncio
    async def test_get_execution_artifact_returns_none_for_missing(self):
        mgr = ExecutionSessionManager()
        assert await mgr.get_execution_artifact("missing") is None

    @pytest.mark.asyncio
    async def test_set_eta_updates_session(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        updated = await mgr.set_eta(session.id, 120)
        assert updated.eta_seconds == 120

    @pytest.mark.asyncio
    async def test_set_eta_returns_none_for_missing(self):
        mgr = ExecutionSessionManager()
        assert await mgr.set_eta("missing", 120) is None

    @pytest.mark.asyncio
    async def test_delete_session_removes_session(self):
        mgr = ExecutionSessionManager()
        session = await mgr.create_session("g1")
        assert await mgr.delete_session(session.id) is True
        assert await mgr.get_session(session.id) is None

    @pytest.mark.asyncio
    async def test_delete_session_returns_false_for_missing(self):
        mgr = ExecutionSessionManager()
        assert await mgr.delete_session("missing") is False
