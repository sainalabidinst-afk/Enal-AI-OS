"""
Knowledge K2 — Hybrid Retrieval & Context Builder
===================================================

Builds on Knowledge K1 (Knowledge Graph + Registry + Evidence).

Provides:
- HybridRetrieval: combines graph similarity, registry search, and evidence lookup
- ContextBuilder: constructs structured context from retrieved knowledge
- KnowledgeContext: standardized output contract

Design:
    Query
        ↓
    HybridRetrieval
        ↓
    ├── Graph similarity
    ├── Registry search
    └── Evidence lookup
        ↓
    ContextBuilder
        ↓
    KnowledgeContext
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from backend.app.core.knowledge.evidence import EvidenceStore
from backend.app.core.knowledge.graph import KnowledgeGraph
from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.retrieval import KnowledgeRetrieval

logger = logging.getLogger(__name__)


# ─── Data Classes ───


@dataclass
class KnowledgeContext:
    """Structured context from knowledge retrieval."""

    query: str
    primary_concepts: list[dict[str, Any]] = field(default_factory=list)
    related_concepts: list[dict[str, Any]] = field(default_factory=list)
    supporting_evidence: list[dict[str, Any]] = field(default_factory=list)
    contradicting_evidence: list[dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    sources: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "primary_concepts": self.primary_concepts,
            "related_concepts": self.related_concepts,
            "supporting_evidence": self.supporting_evidence,
            "contradicting_evidence": self.contradicting_evidence,
            "confidence": self.confidence,
            "sources": self.sources,
            "metadata": self.metadata,
        }


# ─── Hybrid Retrieval ───


class HybridRetrieval:
    """Combines graph, registry, and evidence retrieval strategies."""

    def __init__(
        self,
        retrieval: KnowledgeRetrieval,
        registry: KnowledgeRegistry,
        graph: KnowledgeGraph,
        evidence_store: EvidenceStore,
    ) -> None:
        self._retrieval = retrieval
        self._registry = registry
        self._graph = graph
        self._evidence_store = evidence_store

    def search(
        self,
        query: str,
        domain: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Hybrid search across graph and registry."""
        graph_results = self._retrieval.search(query, domain=domain, limit=limit)
        registry_results = self._registry.find_by_name(query)
        if domain:
            try:
                domain_enum = next(d for d in self._registry.domains() if d.value == domain)
                registry_results = self._registry.find_by_domain(domain_enum)
            except StopIteration:
                pass

        merged: dict[str, dict[str, Any]] = {}
        for item in graph_results:
            merged[item["id"]] = item
        for entity in registry_results:
            if entity.id not in merged:
                merged[entity.id] = {
                    "id": entity.id,
                    "name": entity.name,
                    "description": entity.description,
                    "domain": entity.domain.value,
                    "category": entity.category.value,
                    "type": entity.type.value,
                    "confidence": entity.confidence,
                    "score": 0.0,
                    "entity": entity,
                }
        results = list(merged.values())
        results.sort(key=lambda item: item.get("score", 0), reverse=True)
        return results[:limit]

    def related(
        self,
        concept_id: str,
        relation: str | None = None,
        max_depth: int = 2,
    ) -> list[dict[str, Any]]:
        """Get related concepts from graph."""
        return self._retrieval.related(concept_id, relation=relation, max_depth=max_depth)

    def evidence_for(self, concept_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Get supporting and contradicting evidence for a concept."""
        entries = self._evidence_store.get(concept_id)
        supporting: list[dict[str, Any]] = []
        contradicting: list[dict[str, Any]] = []
        for entry in entries:
            item = {
                "claim_id": entry.claim_id,
                "content": entry.content,
                "source": entry.source,
                "confidence": entry.confidence,
                "timestamp": entry.timestamp.isoformat(),
            }
            if concept_id in entry.contradicting_ids:
                contradicting.append(item)
            else:
                supporting.append(item)
        return supporting, contradicting


# ─── Context Builder ───


class ContextBuilder:
    """Builds structured KnowledgeContext from retrieval results."""

    def __init__(self, hybrid: HybridRetrieval) -> None:
        self._hybrid = hybrid

    def build(
        self,
        query: str,
        domain: str | None = None,
        limit: int = 5,
    ) -> KnowledgeContext:
        """Build knowledge context for a query."""
        primary = self._hybrid.search(query, domain=domain, limit=limit)
        primary_concepts: list[dict[str, Any]] = []
        related_concepts: list[dict[str, Any]] = []
        supporting_evidence: list[dict[str, Any]] = []
        contradicting_evidence: list[dict[str, Any]] = []
        sources: list[str] = []

        for item in primary:
            concept = {
                "id": item["id"],
                "name": item["name"],
                "description": item.get("description", ""),
                "domain": item.get("domain", ""),
                "category": item.get("category", ""),
                "type": item.get("type", ""),
                "confidence": item.get("confidence", 0.0),
                "score": item.get("score", 0.0),
            }
            primary_concepts.append(concept)
            sources.append(item.get("name", item["id"]))

            related = self._hybrid.related(item["id"])
            for rel in related:
                if rel["id"] not in [c["id"] for c in primary_concepts + related_concepts]:
                    related_concepts.append(rel)

            support, contradict = self._hybrid.evidence_for(item["id"])
            supporting_evidence.extend(support)
            contradicting_evidence.extend(contradict)

        confidence = 0.0
        if primary_concepts:
            confidence = sum(c.get("confidence", 0.0) for c in primary_concepts) / len(primary_concepts)

        return KnowledgeContext(
            query=query,
            primary_concepts=primary_concepts,
            related_concepts=related_concepts,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence,
            confidence=confidence,
            sources=sources,
            metadata={
                "domain": domain,
                "limit": limit,
                "primary_count": len(primary_concepts),
                "related_count": len(related_concepts),
            },
        )


# ─── Singleton ───

def create_knowledge_retrieval() -> HybridRetrieval:
    """Factory for HybridRetrieval with default knowledge components."""
    registry = KnowledgeRegistry()
    graph = KnowledgeGraph()
    evidence_store = EvidenceStore()
    retrieval = KnowledgeRetrieval(registry, graph)
    return HybridRetrieval(
        retrieval=retrieval,
        registry=registry,
        graph=graph,
        evidence_store=evidence_store,
    )


def create_context_builder() -> ContextBuilder:
    """Factory for ContextBuilder with default HybridRetrieval."""
    return ContextBuilder(create_knowledge_retrieval())
