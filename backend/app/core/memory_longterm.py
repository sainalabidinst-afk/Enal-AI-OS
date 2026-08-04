import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LongTermMemory:
    """Persistent compressed memory stored on the filesystem."""

    def __init__(self, base_path: str = "./workspace/memory/longterm"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def store(self, key: str, value: Any, ttl: int | None = None, session_id: str | None = None, project_id: str | None = None):
        path = self.base_path / f"{key}.json"
        data = {"key": key, "value": value, "created_at": time.time()}
        path.write_text(json.dumps(data, default=str))

    async def retrieve(self, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        path = self.base_path / f"{key}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return data.get("value")

    async def search(self, query: str, limit: int = 10, session_id: str | None = None, project_id: str | None = None) -> list[dict]:
        results: list[dict] = []
        query_lower = query.lower()
        for path in self.base_path.glob("*.json"):
            data = json.loads(path.read_text())
            content = str(data.get("value", ""))
            if query_lower in content.lower():
                results.append({"key": data["key"], "value": data["value"]})
            if len(results) >= limit:
                break
        return results

    async def delete(self, key: str) -> bool:
        path = self.base_path / f"{key}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    async def list_keys(self, pattern: str = "*") -> list[str]:
        return [p.stem for p in self.base_path.glob(f"{pattern}.json")]
