from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class KnowledgeNode:
    id: str
    domain: str
    category: str
    type: str
    name: str
    description: str = ""
    status: str = "draft"
    confidence: float = 0.0
    schema_version: str = "1.0.0"
    knowledge_version: str = "1.0.0"
    created_at: str = ""
    updated_at: str = ""
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    evidence: list[str] = field(default_factory=list)
    related_ids: list[str] = field(default_factory=list)
    source: str | None = None
    owner: str | None = None
    embedding: list[float] | None = None
