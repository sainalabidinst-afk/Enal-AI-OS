import json
import logging
import time
from pathlib import Path
from typing import Any

from backend.app.core.memory_layer import EpisodicMemoryEntry

logger = logging.getLogger(__name__)


class EpisodicMemory:
    """Event and timeline memory with in-memory index and filesystem persistence."""

    def __init__(self, base_path: str = "./workspace/memory/episodic"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._episodes: dict[str, EpisodicMemoryEntry] = {}

    async def store(self, key: str, value: Any, ttl: int | None = None, session_id: str | None = None, project_id: str | None = None):
        if isinstance(value, dict) and "event_type" in value:
            entry = EpisodicMemoryEntry(
                episode_id=key,
                session_id=value.get("session_id", session_id or "default"),
                timestamp=time.time(),
                event_type=value.get("event_type", "generic"),
                content=value.get("content", {}),
                tags=value.get("tags", []),
                importance=value.get("importance", 0.5),
                summary=value.get("summary", ""),
            )
            self._episodes[key] = entry
            self._persist(entry)

    async def retrieve(self, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        return self._episodes.get(key).__dict__ if key in self._episodes else None

    async def search(self, query: str, limit: int = 10, session_id: str | None = None, project_id: str | None = None) -> list[dict]:
        results: list[dict] = []
        query_lower = query.lower()
        entries = list(self._episodes.values())
        if session_id:
            entries = [e for e in entries if e.session_id == session_id]
        for entry in entries:
            if query_lower in entry.event_type.lower() or query_lower in entry.summary.lower():
                results.append({"key": entry.episode_id, "value": entry.__dict__})
            if len(results) >= limit:
                break
        return results

    async def delete(self, key: str) -> bool:
        if key in self._episodes:
            del self._episodes[key]
            (self.base_path / f"{key}.json").unlink(missing_ok=True)
            return True
        return False

    async def list_keys(self, pattern: str = "*") -> list[str]:
        return list(self._episodes.keys())

    def _persist(self, entry: EpisodicMemoryEntry):
        path = self.base_path / f"{entry.episode_id}.json"
        path.write_text(json.dumps(entry.__dict__, default=str))
