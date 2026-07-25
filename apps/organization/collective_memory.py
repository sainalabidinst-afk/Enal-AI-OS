"""
Collective Memory
==================

Organization-level memory that persists across projects.
Includes project memory, team memory, and organizational knowledge.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    id: str
    category: str
    content: Any
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class CollectiveMemory:
    """Shared memory for the organization."""

    def __init__(self):
        self._entries: dict[str, MemoryEntry] = {}
        self._project_memory: dict[str, list[str]] = {}
        self._team_memory: dict[str, list[str]] = {}

    def store(self, category: str, content: Any, metadata: dict[str, Any] | None = None) -> str:
        entry_id = str(uuid.uuid4())
        entry = MemoryEntry(
            id=entry_id,
            category=category,
            content=content,
            metadata=metadata or {},
        )
        self._entries[entry_id] = entry
        logger.debug(f"Memory stored: {category} -> {entry_id}")
        return entry_id

    def recall(self, entry_id: str) -> MemoryEntry | None:
        return self._entries.get(entry_id)

    def recall_by_category(self, category: str) -> list[MemoryEntry]:
        return [e for e in self._entries.values() if e.category == category]

    def store_project_memory(self, project_id: str, entry_id: str) -> None:
        self._project_memory.setdefault(project_id, []).append(entry_id)

    def get_project_memory(self, project_id: str) -> list[MemoryEntry]:
        entry_ids = self._project_memory.get(project_id, [])
        return [self._entries[eid] for eid in entry_ids if eid in self._entries]

    def store_team_memory(self, team_id: str, entry_id: str) -> None:
        self._team_memory.setdefault(team_id, []).append(entry_id)

    def get_team_memory(self, team_id: str) -> list[MemoryEntry]:
        entry_ids = self._team_memory.get(team_id, [])
        return [self._entries[eid] for eid in entry_ids if eid in self._entries]


collective_memory = CollectiveMemory()
