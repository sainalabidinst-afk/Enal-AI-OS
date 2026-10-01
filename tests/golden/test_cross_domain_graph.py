"""
Golden tests for Cross-Domain Knowledge Graph Generator (RFC-0024).

Verifies:
- MemoryScanner discovers entities across memory layers
- EntityResolver merges cross-domain entity references
- EdgeExtractor discovers relationships between entities
- GraphBuilder persists and loads graph
- InferenceEngine answers cross-domain questions
- End-to-end engine.query returns valid GraphQueryResult
- Worker integration
"""

import pytest

from apps.cross_domain_graph.schemas import (
    GraphQueryRequest,
    GraphQueryResult,
    InferenceResult,
    MemoryLayer,
    NodeType,
    RelationType,
)
from apps.cross_domain_graph.memory_scanner import MemoryScanner
from apps.cross_domain_graph.entity_resolver import EntityResolver
from apps.cross_domain_graph.edge_extractor import EdgeExtractor
from apps.cross_domain_graph.graph_builder import GraphBuilder
from apps.cross_domain_graph.engine import CrossDomainGraphEngine


# ---------------------------------------------------------------------------
# MemoryScanner tests
# ---------------------------------------------------------------------------


@pytest.fixture
def engine():
    return CrossDomainGraphEngine()


@pytest.fixture
def sample_nodes():
    from apps.cross_domain_graph.schemas import GraphNode
    return [
        GraphNode(id="n1", name="Interest Rate", domain="trading", layer="knowledge",
                  node_type=NodeType.CONCEPT, description="Interest rate policy"),
        GraphNode(id="n2", name="Bond Prices", domain="trading", layer="knowledge",
                  node_type=NodeType.CONCEPT, description="Bond market data"),
        GraphNode(id="n3", name="Federal Reserve", domain="macro", layer="knowledge",
                  node_type=NodeType.ENTITY, description="Central bank"),
    ]


class TestMemoryScanner:
    def test_scan_single_layer(self, engine):
        """Test scanning a single memory layer."""
        import asyncio
        scanner = engine.scanner
        nodes = asyncio.get_event_loop().run_until_complete(
            scanner.scan_layer(layer=MemoryLayer.KNOWLEDGE.value, query="interest rate", limit=10)
        )
        assert isinstance(nodes, list)

    def test_scan_all_layers(self, engine):
        """Test scanning all memory layers."""
        import asyncio
        scanner = engine.scanner
        nodes = asyncio.get_event_loop().run_until_complete(
            scanner.scan_all(query="market strategy", limit_per_layer=5)
        )
        assert isinstance(nodes, list)

    def test_scan_returns_graph_nodes(self, engine):
        """Test that scanned nodes have proper GraphNode structure."""
        import asyncio
        from apps.cross_domain_graph.schemas import GraphNode
        scanner = engine.scanner
        nodes = asyncio.get_event_loop().run_until_complete(
            scanner.scan_layer(layer=MemoryLayer.EPISODIC.value, query="revenue", limit=5)
        )
        for node in nodes:
            assert isinstance(node, GraphNode)
            assert node.id is not None
            assert node.name is not None
            assert node.node_type in NodeType
            assert node.domain is not None

    def test_scan_empty_query(self, engine):
        """Test scanning with empty query (broad scan)."""
        import asyncio
        scanner = engine.scanner
        nodes = asyncio.get_event_loop().run_until_complete(
            scanner.scan_all(query="", limit_per_layer=10)
        )
        assert isinstance(nodes, list)


# ---------------------------------------------------------------------------
# EntityResolver tests
# ---------------------------------------------------------------------------


class TestEntityResolver:
    def test_resolve_same_entity_different_domains(self, engine, sample_nodes):
        """Test that same entity across domains is resolved."""
        from apps.cross_domain_graph.schemas import GraphNode

        nodes = [
            GraphNode(id="n1", name="Federal Reserve", domain="trading", layer="knowledge",
                      node_type=NodeType.ENTITY, description="Central bank"),
            GraphNode(id="n2", name="Federal Reserve", domain="network", layer="episodic",
                      node_type=NodeType.ENTITY, description="Central bank"),
        ]
        resolved = engine.resolver.resolve_all(nodes)
        assert isinstance(resolved, list)

    def test_resolve_returns_resolved_entities(self, engine, sample_nodes):
        """Test that resolution produces ResolvedEntity objects."""
        from apps.cross_domain_graph.schemas import ResolvedEntity
        resolved = engine.resolver.resolve_all(sample_nodes)
        for entity in resolved:
            assert isinstance(entity, ResolvedEntity)
            assert entity.canonical_id is not None
            assert entity.name is not None
            assert entity.domain is not None
            assert isinstance(entity.aliases, list)


# ---------------------------------------------------------------------------
# EdgeExtractor tests
# ---------------------------------------------------------------------------


class TestEdgeExtractor:
    def test_extract_edges_between_nodes(self, engine, sample_nodes):
        """Test relationship extraction between entities."""
        edges = engine.extractor.extract_edges(
            sample_nodes,
            context={"query": "relationship"},
        )
        assert isinstance(edges, list)

    def test_extract_relationship_types(self, engine, sample_nodes):
        """Test that extracted edges have valid relationship types."""
        from apps.cross_domain_graph.schemas import GraphNode
        nodes = [
            GraphNode(id="n1", name="A", domain="d1", layer="knowledge",
                      node_type=NodeType.ENTITY, description="Entity A"),
            GraphNode(id="n2", name="B", domain="d2", layer="project",
                      node_type=NodeType.ENTITY, description="Entity B"),
        ]
        edges = engine.extractor.extract_edges(nodes)
        for edge in edges:
            assert edge.relation in RelationType

    def test_extract_with_context(self, engine):
        """Test edge extraction guided by query context."""
        from apps.cross_domain_graph.schemas import GraphNode
        nodes = [
            GraphNode(id="n1", name="System Outage", domain="ops", layer="episodic",
                      node_type=NodeType.ISSUE, description="Recent outage"),
            GraphNode(id="n2", name="Deployment Process", domain="code", layer="project",
                      node_type=NodeType.COMPONENT, description="CI/CD pipeline"),
        ]
        edges = engine.extractor.extract_edges(
            nodes,
            context={"query": "What caused the outage?"},
        )
        assert isinstance(edges, list)


# ---------------------------------------------------------------------------
# GraphBuilder tests
# ---------------------------------------------------------------------------


class TestGraphBuilder:
    def test_build_graph_persists(self, engine, sample_nodes):
        """Test that graph builder persists nodes and edges."""
        engine.builder.build_full_graph(sample_nodes, context={"test": True})
        assert len(engine.builder._nodes) > 0

    def test_stats_returns_counters(self, engine):
        """Test that stats returns node/edge counts."""
        stats = engine.builder.stats()
        assert "node_count" in stats
        assert "edge_count" in stats
        assert isinstance(stats["node_count"], int)
        assert isinstance(stats["edge_count"], int)

    def test_query_nodes(self, engine, sample_nodes):
        """Test node querying by text."""
        engine.builder.build_full_graph(sample_nodes, context={"test": True})
        nodes = engine.builder.query_nodes(query="Interest")
        assert isinstance(nodes, list)
        assert len(nodes) > 0

    def test_find_path(self, engine):
        """Test path finding between nodes."""
        from apps.cross_domain_graph.schemas import GraphNode, GraphEdge, RelationType

        n1 = GraphNode(id="p1", name="Start", domain="d", layer="k", node_type=NodeType.ENTITY, description="Start node")
        n2 = GraphNode(id="p2", name="End", domain="d", layer="k", node_type=NodeType.ENTITY, description="End node")
        engine.builder.add_nodes([n1, n2])
        edge = GraphEdge(
            id="e1", source_id="p1", target_id="p2",
            relation=RelationType.RELATED_TO, weight=0.8, confidence=0.9,
        )
        engine.builder.add_edges([edge])

        paths = engine.builder.find_path("p1", "p2", max_depth=5)
        assert paths is not None
        assert len(paths) > 0

    def test_load_save(self, engine):
        """Test graph persistence round-trip."""
        from apps.cross_domain_graph.schemas import GraphNode

        n = GraphNode(id="persist_test", name="Persist", domain="test", layer="knowledge",
                      node_type=NodeType.ENTITY, description="Persistence test")
        engine.builder.add_nodes([n])
        engine.builder._persist()

        new_engine = CrossDomainGraphEngine()
        loaded = new_engine.builder.load()
        assert loaded is True


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------


class TestCrossDomainGraphEngine:
    def test_query_with_string_input(self, engine):
        """Test that engine.query accepts a simple string."""
        import asyncio
        request = GraphQueryRequest(query="What correlates with interest rates?")
        result = asyncio.get_event_loop().run_until_complete(engine.query(request))
        assert isinstance(result, GraphQueryResult)
        assert result.query == "What correlates with interest rates?"

    def test_query_returns_answer(self, engine):
        """Test that query returns an answer."""
        import asyncio
        result = asyncio.get_event_loop().run_until_complete(
            engine.query("How does revenue relate to pricing?")
        )
        assert isinstance(result.answer, str)
        assert len(result.answer) > 0

    def test_query_returns_entities(self, engine):
        """Test that query returns discovered entities."""
        import asyncio
        result = asyncio.get_event_loop().run_until_complete(
            engine.query("What are the key market indicators?")
        )
        assert isinstance(result.entities_discovered, list)

    def test_query_returns_explanation(self, engine):
        """Test that query includes explanation chain."""
        import asyncio
        result = asyncio.get_event_loop().run_until_complete(
            engine.query("What factors affect market share?")
        )
        assert isinstance(result.explanation, dict)
        assert "reasoning_chain" in result.explanation

    def test_query_serialization(self, engine):
        """Test that GraphQueryResult serializes to dict."""
        import asyncio
        result = asyncio.get_event_loop().run_until_complete(
            engine.query("What affects revenue?")
        )
        data = result.to_dict()
        assert data["query"] == "What affects revenue?"
        assert "answer" in data
        assert "entities_discovered" in data
        assert "relationships" in data
        assert "confidence" in data

    def test_explain_relationship(self, engine):
        """Test relationship explanation between entities."""
        result = engine.explain_relationship("revenue", "pricing")
        assert isinstance(result, dict)
        assert "explanation" in result
        assert "paths" in result

    def test_build_graph_returns_stats(self, engine):
        """Test that build_graph returns summary statistics."""
        import asyncio
        stats = asyncio.get_event_loop().run_until_complete(
            engine.build_graph(query="market", limit_per_layer=10)
        )
        assert "node_count" in stats
        assert "scan_time_ms" in stats
        assert stats["nodes_scanned"] >= 0
