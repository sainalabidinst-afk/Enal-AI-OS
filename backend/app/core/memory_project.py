import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ProjectMemory:
    """Project-focused context memory with longer TTL and filesystem persistence."""

    def __init__(self, base_path: str = "./workspace/memory/project"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def store(self, key: str, value: Any, ttl: int | None = None, session_id: str | None = None, project_id: str | None = None):
        pid = project_id or key.split(":")[0] if ":" in key else "default"
        path = self.base_path / f"{pid}" / f"{key}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"key": key, "value": value, "updated_at": time.time()}
        path.write_text(json.dumps(data, default=str))

    async def retrieve(self, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        pid = project_id or key.split(":")[0] if ":" in key else "default"
        path = self.base_path / f"{pid}" / f"{key}.json"
        if path.exists():
            data = json.loads(path.read_text())
            return data.get("value")
        return None

    async def search(self, query: str, limit: int = 10, session_id: str | None = None, project_id: str | None = None) -> list[dict]:
        results: list[dict] = []
        pid = project_id or "*"
        query_lower = query.lower()
        for proj_dir in self.base_path.iterdir():
            if proj_dir.is_dir():
                for file in proj_dir.glob("*.json"):
                    data = json.loads(file.read_text())
                    if query_lower in str(data.get("value", "")).lower():
                        results.append({"key": data["key"], "value": data["value"], "project_id": proj_dir.name})
                        if len(results) >= limit:
                            return results
        return results

    async def delete(self, key: str, project_id: str | None = None) -> bool:
        pid = project_id or key.split(":")[0] if ":" in key else "default"
        path = self.base_path / f"{pid}" / f"{key}.json"
        try:
            path.unlink(missing_ok=True)
            return True
        except Exception:
            return False

    async def list_keys(self, pattern: str = "*", project_id: str | None = None) -> list[str]:
        pid = project_id or "*"
        results: list[str] = []
        for proj_dir in self.base_path.glob(f"{pid}" if pid != "*" else "*"):
            if proj_dir.is_dir():
                for f in proj_dir.glob(f"{pattern}.json"):
                    results.append(f.stem)
        return results
