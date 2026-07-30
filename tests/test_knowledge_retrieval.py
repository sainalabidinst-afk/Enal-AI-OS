"""
Integration Tests for Knowledge K2 — Hybrid Retrieval & Context Builder
=======================================================================

Tests scenarios:
    - hybrid search across graph and registry
    - related concept traversal
    - evidence lookup (supporting and contradicting)
    - context building with primary and related concepts
    - confidence calculation
    - empty results handling
"""

import pytest

from apps.organization.knowledge_retrieval import (
    ContextBuilder,
    HybridRetrieval,
    KnowledgeContext,
    create_context_builder,
    create_knowledge_retrieval,
)
from backend.app.core.knowledge.evidence import EvidenceStore, EvidenceBuilder
from backend.app.core.knowledge.graph import KnowledgeGraph, KnowledgeNode
from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.retrieval import KnowledgeRetrieval
from backend.app.core.knowledge.schema import (
    KnowledgeCategory,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeStatus,
    KnowledgeType,
)


# ─── Fixtures ───


@pytest.fixture
def registry() -> KnowledgeRegistry:
    return KnowledgeRegistry()


@pytest.fixture
def graph() -> KnowledgeGraph:
    return KnowledgeGraph()


@pytest.fixture
def evidence_store() -> EvidenceStore:
    return EvidenceStore()


@pytest.fixture
def retrieval(registry: KnowledgeRegistry, graph: KnowledgeGraph) -> KnowledgeRetrieval:
    return KnowledgeRetrieval(registry, graph)


@pytest.fixture
def hybrid(retrieval: KnowledgeRetrieval, registry: KnowledgeRegistry, graph: KnowledgeGraph, evidence_store: EvidenceStore) -> HybridRetrieval:
    return HybridRetrieval(retrieval, registry, graph, evidence_store)


@pytest.fixture
def context_builder(hybrid: HybridRetrieval) -> ContextBuilder:
    return ContextBuilder(hybrid)


@pytest.fixture
def populated_knowledge(registry: KnowledgeRegistry, graph: KnowledgeGraph):
    """Populate registry and graph with sample knowledge."""
    entity1 = KnowledgeEntity(
        id="concept-1",
        domain=KnowledgeDomain.CODE,
        category=KnowledgeCategory.DOMAIN,
        type=KnowledgeType.CONCEPT,
        name="Clean Architecture",
        description="Software architecture pattern with layered dependencies",
        status=KnowledgeStatus.VALIDATED,
        confidence=0.9,
        tags=["architecture", "clean-code", "layers"],
    )
    entity2 = KnowledgeEntity(
        id="concept-2",
        domain=KnowledgeDomain.CODE,
        category=KnowledgeCategory.DOMAIN,
        type=KnowledgeType.CONCEPT,
        name="Dependency Injection",
        description="Design pattern for loose coupling",
        status=KnowledgeStatus.VALIDATED,
        confidence=0.85,
        tags=["architecture", "di", "coupling"],
    )
    entity3 = KnowledgeEntity(
        id="concept-3",
        domain=KnowledgeDomain.TRADING,
        category=KnowledgeCategory.DOMAIN,
        type=KnowledgeType.CONCEPT,
        name="Market Structure",
        description="Price action patterns and market phases",
        status=KnowledgeStatus.VALIDATED,
        confidence=0.8,
        tags=["trading", "price-action", "patterns"],
    )
    registry.register(entity1)
    registry.register(entity2)
    registry.register(entity3)

    node1 = KnowledgeNode(
        id="concept-1",
        domain=KnowledgeDomain.CODE.value,
        category=KnowledgeCategory.DOMAIN.value,
        type=KnowledgeType.CONCEPT.value,
        name="Clean Architecture",
        description="Software architecture pattern with layered dependencies",
        status=KnowledgeStatus.VALIDATED.value,
        confidence=0.9,
        tags=["architecture", "clean-code", "layers"],
    )
    node2 = KnowledgeNode(
        id="concept-2",
        domain=KnowledgeDomain.CODE.value,
        category=KnowledgeCategory.DOMAIN.value,
        type=KnowledgeType.CONCEPT.value,
        name="Dependency Injection",
        description="Design pattern for loose coupling",
        status=KnowledgeStatus.VALIDATED.value,
        confidence=0.85,
        tags=["architecture", "di", "coupling"],
    )
    graph.add_node(node1)
    graph.add_node(node2)
    return registry, graph


# ─── Tests: HybridRetrieval ───


def test_hybrid_search_by_name(hybrid: HybridRetrieval, populated_knowledge):
    registry, graph = populated_knowledge
    results = hybrid.search("Clean Architecture")
    assert len(results) >= 1
    assert results[0]["name"] == "Clean Architecture"


def test_hybrid_search_by_domain(hybrid: HybridRetrieval, populated_knowledge):
    registry, graph = populated_knowledge
    results = hybrid.search("architecture", domain="code")
    assert len(results) >= 1
    for item in results:
        assert item["domain"] == "code"


def test_hybrid_search_empty(hybrid: HybridRetrieval):
    results = hybrid.search("nonexistent concept xyz")
    assert results == []


def test_hybrid_related(hybrid: HybridRetrieval, populated_knowledge):
    registry, graph = populated_knowledge
    related = hybrid.related("concept-1")
    assert isinstance(related, list)
    assert len(related) >= 0


def test_evidence_for_concept(hybrid: HybridRetrieval, evidence_store: EvidenceStore):
    builder = EvidenceBuilder("claim-1")
    builder.add("Clean Architecture improves maintainability", "test", confidence=0.9)
    for ev in builder.build():
        evidence_store.add(ev)
    support, contradict = hybrid.evidence_for("claim-1")
    assert len(support) == 1
    assert len(contradict) == 0
    assert support[0]["content"] == "Clean Architecture improves maintainability"


# ─── Tests: ContextBuilder ───


def test_context_builder_builds_context(context_builder: ContextBuilder, populated_knowledge):
    registry, graph = populated_knowledge
    ctx = context_builder.build("Clean Architecture", domain="code")
    assert isinstance(ctx, KnowledgeContext)
    assert ctx.query == "Clean Architecture"
    assert len(ctx.primary_concepts) >= 1
    assert ctx.confidence >= 0.0


def test_context_builder_empty_query(context_builder: ContextBuilder):
    ctx = context_builder.build("nonexistent xyz")
    assert ctx.query == "nonexistent xyz"
    assert ctx.primary_concepts == []
    assert ctx.confidence == 0.0


def test_context_builder_to_dict(context_builder: ContextBuilder, populated_knowledge):
    registry, graph = populated_knowledge
    ctx = context_builder.build("Clean Architecture")
    data = ctx.to_dict()
    assert "query" in data
    assert "primary_concepts" in data
    assert "related_concepts" in data
    assert "supporting_evidence" in data
    assert "contradicting_evidence" in data
    assert "confidence" in data
    assert "sources" in data


def test_context_builder_includes_related(context_builder: ContextBuilder, populated_knowledge):
    registry, graph = populated_knowledge
    ctx = context_builder.build("Clean Architecture", limit=3)
    assert "metadata" in ctx.to_dict()
    assert "related_count" in ctx.metadata


# ─── Tests: Factory Functions ───


def test_create_knowledge_retrieval():
    hybrid = create_knowledge_retrieval()
    assert isinstance(hybrid, HybridRetrieval)


def test_create_context_builder():
    builder = create_context_builder()
    assert isinstance(builder, ContextBuilder)
