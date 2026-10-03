"""
Blueprint repository for visual builder persistence.

Stores agent and tool blueprints in memory with optional
PostgreSQL persistence for multi-session durability.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BlueprintRepository:
    """In-memory blueprint store with JSON file persistence."""

    def __init__(self, storage_path: str | Path = "data/blueprints") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._agents: dict[str, dict[str, Any]] = {}
        self._tools: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        for kind, store in (("agents", self._agents), ("tools", self._tools)):
            file_path = self.storage_path / f"{kind}.json"
            if file_path.exists():
                try:
                    data = json.loads(file_path.read_text(encoding="utf-8"))
                    store.update(data)
                except (json.JSONDecodeError, OSError) as e:
                    logger.warning("Failed to load %s: %s", file_path, e)

    def _save(self, kind: str) -> None:
        file_path = self.storage_path / f"{kind}.json"
        store = self._agents if kind == "agents" else self._tools
        try:
            file_path.write_text(
                json.dumps(store, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as e:
            logger.error("Failed to save %s: %s", file_path, e)

    def create_agent(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        blueprint_id = blueprint.get("id") or str(uuid.uuid4())
        blueprint["id"] = blueprint_id
        blueprint["created_at"] = datetime.now(UTC).isoformat()
        blueprint["updated_at"] = blueprint["created_at"]
        self._agents[blueprint_id] = blueprint
        self._save("agents")
        return blueprint

    def update_agent(self, blueprint_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        existing = self._agents.get(blueprint_id)
        if not existing:
            return None
        existing.update(updates)
        existing["updated_at"] = datetime.now(UTC).isoformat()
        self._save("agents")
        return existing

    def get_agent(self, blueprint_id: str) -> dict[str, Any] | None:
        return self._agents.get(blueprint_id)

    def list_agents(self) -> list[dict[str, Any]]:
        return list(self._agents.values())

    def delete_agent(self, blueprint_id: str) -> bool:
        if blueprint_id in self._agents:
            del self._agents[blueprint_id]
            self._save("agents")
            return True
        return False

    def create_tool(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        blueprint_id = blueprint.get("id") or str(uuid.uuid4())
        blueprint["id"] = blueprint_id
        blueprint["created_at"] = datetime.now(UTC).isoformat()
        blueprint["updated_at"] = blueprint["created_at"]
        self._tools[blueprint_id] = blueprint
        self._save("tools")
        return blueprint

    def update_tool(self, blueprint_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        existing = self._tools.get(blueprint_id)
        if not existing:
            return None
        existing.update(updates)
        existing["updated_at"] = datetime.now(UTC).isoformat()
        self._save("tools")
        return existing

    def get_tool(self, blueprint_id: str) -> dict[str, Any] | None:
        return self._tools.get(blueprint_id)

    def list_tools(self) -> list[dict[str, Any]]:
        return list(self._tools.values())

    def delete_tool(self, blueprint_id: str) -> bool:
        if blueprint_id in self._tools:
            del self._tools[blueprint_id]
            self._save("tools")
            return True
        return False


blueprint_repository = BlueprintRepository()
