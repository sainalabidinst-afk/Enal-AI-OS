from __future__ import annotations

from typing import Any
from backend.app.core.knowledge.evidence import EvidenceBuilder, EvidenceStore
from backend.app.core.knowledge.graph import KnowledgeGraph
from backend.app.core.knowledge.learning import LearningEngine
from backend.app.core.knowledge.ontology import Ontology
from backend.app.core.knowledge.reference import Reference, ReferenceStore
from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.retrieval import KnowledgeRetrieval
from backend.app.core.knowledge.schema import KnowledgeEntity
from backend.app.core.knowledge.store import KnowledgeStore


class CapabilityKnowledgeBridge:
    def __init__(self, knowledge_store: KnowledgeStore) -> None:
        self.store = knowledge_store
        self.registry = knowledge_store.registry
        self.graph = knowledge_store.graph
        self.evidence = knowledge_store.evidence
        self.retrieval = KnowledgeRetrieval(self.registry, self.graph)
        self.learning = LearningEngine()
        self.ontology = Ontology()
        self.references = ReferenceStore()

    def register_finding(self, entity: KnowledgeEntity) -> KnowledgeEntity:
        return self.store.register(entity)

    def add_evidence(self, claim_id: str, content: str, source: str, confidence: float, capability: str | None = None, metadata: dict[str, Any] | None = None) -> EvidenceBuilder:
        builder = EvidenceBuilder(claim_id=claim_id, capability=capability)
        builder.add(content=content, source=source, confidence=confidence, metadata=metadata)
        for item in builder.build():
            self.evidence.add(item)
        return builder

    def record_experience(self, domain: str, context: dict[str, Any], action: str, outcome: str, success: bool, confidence: float = 0.0) -> None:
        if success:
            self.learning.record_success(domain=domain, context=context, action_taken=action, outcome=outcome, confidence=confidence)
        else:
            self.learning.record_failure(domain=domain, context=context, action_taken=action, failure_reason=outcome, confidence=confidence)

    def recommend(self, domain: str, context: dict[str, Any]) -> dict[str, Any] | None:
        rec = self.learning.recommend(domain=domain, context=context)
        if not rec:
            return None
        return {
            "recommendation_id": rec.recommendation_id,
            "domain": rec.domain,
            "suggestion": rec.suggestion,
            "rationale": rec.rationale,
            "confidence": rec.confidence,
            "based_on_patterns": rec.based_on_patterns,
            "based_on_lessons": rec.based_on_lessons,
        }

    def search_knowledge(self, query: str, domain: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        return self.retrieval.search(query, domain=domain, limit=limit)

    def related_concepts(self, concept_id: str, relation: str | None = None, max_depth: int = 2) -> list[dict[str, Any]]:
        return self.retrieval.related(concept_id, relation=relation, max_depth=max_depth)

    def hybrid_query(self, query: str, domain: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        return self.retrieval.hybrid(query, domain=domain, limit=limit)

    def add_reference(self, reference_id: str, title: str, source: str, content: str, source_type: str = "standard", tags: list[str] | None = None) -> Reference:
        from backend.app.core.knowledge.reference import Reference
        ref = Reference(
            reference_id=reference_id,
            title=title,
            source=source,
            source_type=source_type,
            content=content,
            tags=tags or [],
        )
        return self.references.add(ref)

    def find_references(self, tag: str | None = None, source: str | None = None) -> list[dict[str, Any]]:
        if tag:
            refs = self.references.find_by_tag(tag)
        elif source:
            refs = self.references.find_by_source(source)
        else:
            refs = self.references.all()
        return [
            {
                "reference_id": r.reference_id,
                "title": r.title,
                "source": r.source,
                "source_type": r.source_type,
                "url": r.url,
                "content": r.content,
                "tags": r.tags,
                "confidence": r.confidence,
            }
            for r in refs
        ]
