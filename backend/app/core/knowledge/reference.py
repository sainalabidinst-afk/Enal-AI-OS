from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Reference:
    reference_id: str
    title: str
    source: str
    source_type: str = "standard"
    url: str | None = None
    content: str = ""
    tags: list[str] = field(default_factory=list)
    confidence: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


class ReferenceStore:
    def __init__(self) -> None:
        self._references: dict[str, Reference] = {}

    def add(self, reference: Reference) -> Reference:
        self._references[reference.reference_id] = reference
        return reference

    def get(self, reference_id: str) -> Reference | None:
        return self._references.get(reference_id)

    def find_by_source(self, source: str) -> list[Reference]:
        return [r for r in self._references.values() if r.source == source]

    def find_by_tag(self, tag: str) -> list[Reference]:
        return [r for r in self._references.values() if tag in r.tags]

    def find_by_source_type(self, source_type: str) -> list[Reference]:
        return [r for r in self._references.values() if r.source_type == source_type]

    def search(self, query: str) -> list[Reference]:
        lowered = query.lower()
        return [r for r in self._references.values() if lowered in r.title.lower() or lowered in r.content.lower()]

    def all(self) -> list[Reference]:
        return list(self._references.values())
