import pytest

from backend.app.core.semantic_graph import (
    GraphEdge,
    GraphNode,
    NodeType,
    RelationType,
    SemanticProjectGraph,
)


class TestGraphNode:
    def test_defaults(self):
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="Project", description="desc")
        assert node.properties == {}
        assert node.project_id is None
        assert node.created_at is not None


class TestGraphEdge:
    def test_defaults(self):
        edge = GraphEdge(id="e1", source_id="n1", target_id="n2", relation=RelationType.DEPENDS_ON)
        assert edge.properties == {}


class TestSemanticProjectGraph:
    @pytest.mark.asyncio
    async def test_add_node(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="Project", description="desc")
        node_id = await graph.add_node(node)
        assert node_id == "n1"
        assert graph._nodes["n1"] is node

    @pytest.mark.asyncio
    async def test_add_edge(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        edge_id = await graph.add_edge("n1", "n2", RelationType.DEPENDS_ON)
        assert edge_id.startswith("edge-")
        assert len(graph._edges) == 1

    @pytest.mark.asyncio
    async def test_get_related(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        await graph.add_node(GraphNode(id="n2", node_type=NodeType.PROJECT, name="P2", description="d"))
        await graph.add_edge("n1", "n2", RelationType.DEPENDS_ON)
        related = await graph.get_related("n1")
        assert len(related) == 1
        assert related[0]["target"] == "n2"

    @pytest.mark.asyncio
    async def test_get_related_filters_by_relation(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        await graph.add_node(GraphNode(id="n2", node_type=NodeType.PROJECT, name="P2", description="d"))
        await graph.add_edge("n1", "n2", RelationType.DEPENDS_ON)
        related = await graph.get_related("n1", relation=RelationType.USES)
        assert len(related) == 0

    @pytest.mark.asyncio
    async def test_get_dependencies(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        await graph.add_node(GraphNode(id="n2", node_type=NodeType.PROJECT, name="P2", description="d"))
        await graph.add_edge("n2", "n1", RelationType.DEPENDS_ON)
        deps = await graph.get_dependencies("n1")
        assert len(deps) == 1
        assert deps[0].id == "n2"

    @pytest.mark.asyncio
    async def test_get_dependents(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        await graph.add_node(GraphNode(id="n2", node_type=NodeType.PROJECT, name="P2", description="d"))
        await graph.add_edge("n1", "n2", RelationType.DEPENDS_ON)
        dependents = await graph.get_dependents("n1")
        assert len(dependents) == 1
        assert dependents[0].id == "n2"

    @pytest.mark.asyncio
    async def test_propagate_change(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        await graph.add_node(GraphNode(id="n2", node_type=NodeType.PROJECT, name="P2", description="d"))
        await graph.add_node(GraphNode(id="n3", node_type=NodeType.PROJECT, name="P3", description="d"))
        await graph.add_edge("n1", "n2", RelationType.DEPENDS_ON)
        await graph.add_edge("n2", "n3", RelationType.DEPENDS_ON)
        affected = await graph.propagate_change("n1", {})
        assert "n2" in affected
        assert "n3" in affected

    @pytest.mark.asyncio
    async def test_query_by_name(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="MyProject", description="A project"))
        results = await graph.query("MyProject")
        assert len(results) == 1
        assert results[0]["name"] == "MyProject"

    @pytest.mark.asyncio
    async def test_query_by_description(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="A test project"))
        results = await graph.query("test")
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_query_filters_by_node_type(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        await graph.add_node(GraphNode(id="n2", node_type=NodeType.COMPONENT, name="C1", description="d"))
        results = await graph.query("P1", node_type=NodeType.PROJECT)
        assert len(results) == 1
        assert results[0]["id"] == "n1"

    @pytest.mark.asyncio
    async def test_query_returns_empty_for_no_match(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        await graph.add_node(GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d"))
        results = await graph.query("nonexistent")
        assert results == []

    @pytest.mark.asyncio
    async def test_get_evidence(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d", properties={"sources": [{"confidence": 0.8, "url": "http://test.com"}]})
        await graph.add_node(node)
        evidence = await graph.get_evidence("n1")
        assert evidence is not None
        assert evidence["node_id"] == "n1"
        assert "evidence_score" in evidence

    @pytest.mark.asyncio
    async def test_get_evidence_returns_none_for_missing(self, tmp_path):
        graph = SemanticProjectGraph(base_path=str(tmp_path))
        assert await graph.get_evidence("missing") is None

    def test_calculate_evidence_score_no_sources(self):
        graph = SemanticProjectGraph()
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d")
        score = graph._calculate_evidence_score(node)
        assert score == 0.5

    def test_calculate_evidence_score_with_sources(self):
        graph = SemanticProjectGraph()
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d", properties={"sources": [{"confidence": 0.8}, {"confidence": 0.6}]})
        score = graph._calculate_evidence_score(node)
        assert score == 0.7

    def test_format_citation_with_url(self):
        graph = SemanticProjectGraph()
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d", properties={"sources": [{"url": "http://test.com"}]})
        citation = graph._format_citation(node)
        assert "http://test.com" in citation

    def test_format_citation_with_document(self):
        graph = SemanticProjectGraph()
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d", properties={"sources": [{"document": "doc.pdf"}]})
        citation = graph._format_citation(node)
        assert "doc.pdf" in citation

    def test_format_citation_no_sources(self):
        graph = SemanticProjectGraph()
        node = GraphNode(id="n1", node_type=NodeType.PROJECT, name="P1", description="d")
        citation = graph._format_citation(node)
        assert citation == "Internal knowledge: P1"
