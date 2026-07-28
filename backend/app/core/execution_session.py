import asyncio
from datetime import UTC, datetime
from typing import Any

from backend.app.models.schemas_execution import (
    ExecutionArtifact,
    ExecutionPhase,
    ExecutionSession,
    ExecutionStatus,
)


class ExecutionSessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, ExecutionSession] = {}
        self._execution_artifacts: dict[str, ExecutionArtifact] = {}
        self._lock = asyncio.Lock()

    async def create_session(self, goal: str, conversation_id: str | None = None, workspace_id: str | None = None) -> ExecutionSession:
        async with self._lock:
            session = ExecutionSession(goal=goal, conversation_id=conversation_id, workspace_id=workspace_id)
            self._sessions[session.id] = session
            return session

    async def get_session(self, session_id: str) -> ExecutionSession | None:
        return self._sessions.get(session_id)

    async def list_sessions(self, workspace_id: str | None = None) -> list[ExecutionSession]:
        if workspace_id:
            return [s for s in self._sessions.values() if s.workspace_id == workspace_id]
        return list(self._sessions.values())

    async def update_status(self, session_id: str, status: ExecutionStatus, error: str | None = None) -> ExecutionSession | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        session.status = status
        session.updated_at = datetime.now(UTC)
        if status == ExecutionStatus.completed:
            session.completed_at = datetime.now(UTC)
            session.progress = 100.0
        if error:
            session.error = error
        return session

    async def update_progress(self, session_id: str, progress: float, eta_seconds: int | None = None) -> ExecutionSession | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        session.progress = max(0.0, min(100.0, progress))
        session.updated_at = datetime.now(UTC)
        if eta_seconds is not None:
            session.eta_seconds = eta_seconds
        return session

    async def add_phase(self, session_id: str, name: str) -> dict[str, Any] | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        phase = ExecutionPhase(id=f"{session_id}-{len(session.phases)+1}", name=name, status=ExecutionStatus.pending)
        session.phases.append(phase.model_dump())
        session.updated_at = datetime.now(UTC)
        return phase.model_dump()

    async def update_phase(self, session_id: str, phase_id: str, status: ExecutionStatus, progress: float | None = None) -> dict[str, Any] | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        for idx, raw_phase in enumerate(session.phases):
            if raw_phase.get("id") == phase_id:
                updated = dict(raw_phase)
                updated["status"] = status
                if progress is not None:
                    updated["progress"] = max(0.0, min(100.0, progress))
                if status == ExecutionStatus.running:
                    updated["started_at"] = datetime.now(UTC)
                if status == ExecutionStatus.completed:
                    updated["completed_at"] = datetime.now(UTC)
                    updated["progress"] = 100.0
                session.phases[idx] = updated
                session.updated_at = datetime.now(UTC)
                return updated
        return None

    async def add_log(self, session_id: str, message: str, level: str = "info", metadata: dict[str, Any] | None = None) -> dict[str, Any] | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        entry: dict[str, Any] = {"timestamp": datetime.now(UTC).isoformat(), "level": level, "message": message}
        if metadata:
            entry["metadata"] = metadata
        session.logs.append(entry)
        session.updated_at = datetime.now(UTC)
        return entry

    async def add_artifact(self, session_id: str, name: str, artifact_type: str, content: str | None = None, path: str | None = None, metadata: dict[str, Any] | None = None) -> ExecutionArtifact | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        artifact = ExecutionArtifact(execution_id=session_id, name=name, type=artifact_type, content=content, path=path, metadata=metadata or {})
        session.artifacts.append(artifact.id)
        self._execution_artifacts[artifact.id] = artifact
        session.updated_at = datetime.now(UTC)
        return artifact

    async def get_execution_artifact(self, artifact_id: str) -> ExecutionArtifact | None:
        return self._execution_artifacts.get(artifact_id)

    async def set_eta(self, session_id: str, eta_seconds: int) -> ExecutionSession | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        session.eta_seconds = eta_seconds
        session.updated_at = datetime.now(UTC)
        return session

    async def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False


execution_session_manager = ExecutionSessionManager()
