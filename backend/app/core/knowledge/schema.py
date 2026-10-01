from __future__ import annotations  # noqa: I001

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum, Enum  # noqa: F401
from typing import Any

KNOWLEDGE_SCHEMA_VERSION = "1.0.0"


class KnowledgeDomain(StrEnum):
    TRADING = "trading"
    NETWORK = "network"
    CODE = "code"
    SECURITY = "security"
    DEVOPS = "devops"
    RESEARCH = "research"
    OPERATIONS = "operations"
    REFERENCE = "reference"
    EXPERIENCE = "experience"
    INFRASTRUCTURE = "infrastructure"


class KnowledgeCategory(StrEnum):
    DOMAIN = "domain"
    OPERATIONAL = "operational"
    REFERENCE = "reference"
    LEARNED = "learned"
    EXPERIENCE = "experience"
    EVIDENCE = "evidence"
    ONTOLOGY = "ontology"


class KnowledgeStatus(StrEnum):
    DRAFT = "draft"
    VALIDATED = "validated"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class KnowledgeType(StrEnum):
    CONCEPT = "concept"
    RELATION = "relation"
    RULE = "rule"
    PROCEDURE = "procedure"
    PATTERN = "pattern"
    EVIDENCE = "evidence"
    LESSON = "lesson"
    REFERENCE = "reference"


@dataclass
class KnowledgeEntity:
    id: str
    domain: KnowledgeDomain
    category: KnowledgeCategory
    type: KnowledgeType
    name: str
    description: str = ""
    status: KnowledgeStatus = KnowledgeStatus.DRAFT
    confidence: float = 0.0
    schema_version: str = field(default_factory=lambda: KNOWLEDGE_SCHEMA_VERSION)
    knowledge_version: str = field(default_factory=lambda: "1.0.0")
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    evidence: list[str] = field(default_factory=list)
    related_ids: list[str] = field(default_factory=list)
    source: str | None = None
    owner: str | None = None

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)
