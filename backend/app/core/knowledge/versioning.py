from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class KnowledgeVersion:
    entity_id: str
    version: str
    changed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    changed_by: str | None = None
    change_summary: str = ""
    snapshot: dict[str, Any] = field(default_factory=dict)


class KnowledgeVersionStore:
    def __init__(self) -> None:
        self._history: dict[str, list[KnowledgeVersion]] = {}

    def record(self, version: KnowledgeVersion) -> None:
        self._history.setdefault(version.entity_id, []).append(version)

    def history(self, entity_id: str) -> list[KnowledgeVersion]:
        return list(self._history.get(entity_id, []))

    def latest(self, entity_id: str) -> KnowledgeVersion | None:
        history = self._history.get(entity_id)
        return history[-1] if history else None
