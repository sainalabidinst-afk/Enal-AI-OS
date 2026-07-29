from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from backend.app.core.knowledge.evidence import Evidence, EvidenceStore
from backend.app.core.knowledge.graph import KnowledgeGraph
from backend.app.core.knowledge.node import KnowledgeNode
from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.schema import (
    KnowledgeCategory,
    KnowledgeDomain,
    KnowledgeEntity,
)


@dataclass
class KnowledgeStore:
    registry: KnowledgeRegistry = field(default_factory=KnowledgeRegistry)
    graph: KnowledgeGraph = field(default_factory=KnowledgeGraph)
    evidence: EvidenceStore = field(default_factory=EvidenceStore)

    def register(self, entity: KnowledgeEntity) -> KnowledgeEntity:
        self.registry.register(entity)
        node = KnowledgeNode(
            id=entity.id,
            domain=entity.domain.value,
            category=entity.category.value,
            type=entity.type.value,
            name=entity.name,
            description=entity.description,
            status=entity.status.value,
            confidence=entity.confidence,
            schema_version=entity.schema_version,
            knowledge_version=entity.knowledge_version,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
            tags=list(entity.tags),
            metadata=dict(entity.metadata),
            evidence=list(entity.evidence),
            related_ids=list(entity.related_ids),
            source=entity.source,
            owner=entity.owner,
        )
        self.graph.add_node(node)
        return entity

    def resolve(self, entity_id: str) -> KnowledgeEntity | None:
        return self.registry.resolve(entity_id)

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence.add(evidence)

    def get_evidence(self, claim_id: str) -> list[Evidence]:
        return self.evidence.get(claim_id)

    def confidence(self, claim_id: str) -> float:
        return self.evidence.confidence(claim_id)

    def find_by_domain(self, domain: KnowledgeDomain) -> list[KnowledgeEntity]:
        return self.registry.find_by_domain(domain)

    def find_by_category(self, category: KnowledgeCategory) -> list[KnowledgeEntity]:
        return self.registry.find_by_category(category)

    def find_by_tag(self, tag: str) -> list[KnowledgeEntity]:
        return self.registry.find_by_tag(tag)

    def find_by_name(self, query: str) -> list[KnowledgeEntity]:
        return self.registry.find_by_name(query)

    def all(self) -> list[KnowledgeEntity]:
        return self.registry.all()
