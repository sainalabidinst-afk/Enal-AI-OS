import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class KnowledgeMemory:
    """Keyword-indexed knowledge memory stored on the filesystem."""

    def __init__(self, base_path: str = "./workspace/memory/knowledge"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, list[str]] = {}

    async def store(self, key: str, value: Any, ttl: int | None = None, session_id: str | None = None, project_id: str | None = None):
        path = self.base_path / f"{key}.json"
        data = {"key": key, "value": value, "updated_at": time.time()}
        path.write_text(json.dumps(data, default=str))
        content = str(value).lower()
        words = [w for w in content.split() if len(w) > 3]
        self._index[key] = words

    async def retrieve(self, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        path = self.base_path / f"{key}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return data.get("value")

    async def search(self, query: str, limit: int = 10, session_id: str | None = None, project_id: str | None = None) -> list[dict]:
        query_lower = query.lower()
        results: list[dict] = []
        for path in self.base_path.glob("*.json"):
            data = json.loads(path.read_text())
            score = sum(1 for w in data.get("value", "").lower().split() if query_lower in w)
            if score > 0:
                results.append({"key": data["key"], "value": data["value"], "score": score})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    async def delete(self, key: str) -> bool:
        path = self.base_path / f"{key}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    async def list_keys(self, pattern: str = "*") -> list[str]:
        return [p.stem for p in self.base_path.glob(f"{pattern}.json")]
