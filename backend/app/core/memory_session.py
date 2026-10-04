import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SessionMemory:
    """Conversation-based context memory with filesystem persistence."""

    def __init__(self, base_path: str = "./workspace/memory/session"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._sessions: dict[str, dict] = {}
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Load persisted sessions from filesystem into in-memory cache."""
        for path in self.base_path.glob("*.json"):
            try:
                session_id = path.stem
                self._sessions[session_id] = json.loads(path.read_text())
            except json.JSONDecodeError:
                logger.warning(f"Failed to load session from {path}")

    async def store(
        self,
        key: str,
        value: Any,
        ttl: int | None = 86400,
        session_id: str | None = None,
        project_id: str | None = None,
    ):  # noqa: E501
        sid = session_id or key.split(":")[0] if ":" in key else key
        if sid not in self._sessions:
            self._sessions[sid] = {}
        self._sessions[sid][key] = {"value": value, "timestamp": time.time()}
        self._persist_session(sid)

    async def retrieve(
        self, key: str, session_id: str | None = None, project_id: str | None = None
    ) -> Any | None:  # noqa: E501
        sid = session_id or key.split(":")[0] if ":" in key else key
        return self._sessions.get(sid, {}).get(key, {}).get("value")

    async def search(
        self,
        query: str,
        limit: int = 10,
        session_id: str | None = None,
        project_id: str | None = None,
    ) -> list[dict]:  # noqa: E501
        results: list[dict] = []
        query_lower = query.lower()
        sessions = (
            {session_id: self._sessions.get(session_id, {})} if session_id else self._sessions
        )  # noqa: E501
        for sid, session in sessions.items():
            for k, v in session.items():
                if query_lower in str(v.get("value", "")).lower():
                    results.append({"key": k, "value": v.get("value"), "session_id": sid})
            if len(results) >= limit:
                break
        return results

    async def delete(self, key: str, session_id: str | None = None) -> bool:
        sid = session_id or key.split(":")[0] if ":" in key else key
        if sid in self._sessions and key in self._sessions[sid]:
            del self._sessions[sid][key]
            self._persist_session(sid)
            return True
        return False

    async def list_keys(self, pattern: str = "*", session_id: str | None = None) -> list[str]:
        import fnmatch

        if session_id and session_id in self._sessions:
            session_keys = list(self._sessions[session_id].keys())
            return [k for k in session_keys if fnmatch.fnmatch(k, pattern)]
        if session_id:
            return []
        results: list[str] = []
        for sid, session in self._sessions.items():
            for k in session.keys():
                if fnmatch.fnmatch(k, pattern):
                    results.append(k)
        return results

    def _persist_session(self, session_id: str):
        path = self.base_path / f"{session_id}.json"
        path.write_text(json.dumps(self._sessions.get(session_id, {}), default=str))

    def load_session(self, session_id: str) -> bool:
        path = self.base_path / f"{session_id}.json"
        if path.exists():
            self._sessions[session_id] = json.loads(path.read_text())
            return True
        return False
