"""
Graph Builder — builds and maintains the cross-domain knowledge graph.

Manages the persistent storage of nodes and edges, supports incremental
updates, and provides traversal queries.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

from apps.cross_domain_graph.edge_extractor import EdgeExtractor
from apps.cross_domain_graph.entity_resolver import EntityResolver
from apps.cross_domain_graph.schemas import (
    GraphEdge,
    GraphNode,
    InferenceResult,
    NodeType,
    RelationType,
    ResolvedEntity,
)

logger = logging.getLogger(__name__)


class GraphBuilder:
    """
    Builds and maintains the cross-domain knowledge graph.

    Usage::

        builder = GraphBuilder(persist_path="./workspace/graph")
        builder.add_nodes(nodes)
        builder.add_edges(edges)
        result = builder.query("What correlates with X?")
    """

    def __init__(
        self,
        persist_path: str = "./workspace/cross_domain_graph",
        resolver: EntityResolver | None = None,
        extractor: EdgeExtractor | None = None,
    ) -> None:
        self.persist_path = Path(persist_path)
        self.persist_path.mkdir(parents=True, exist_ok=True)
        self._resolver = resolver or EntityResolver()
        self._extractor = extractor or EdgeExtractor(self._resolver)

        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._resolved: dict[str, ResolvedEntity] = {}
        self._adjacency: dict[str, list[str]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def add_nodes(self, nodes: list[GraphNode]) -> int:
        """Add nodes to the graph, returning count added."""
        count = 0
        for node in nodes:
            if node.id in self._nodes:
                # Merge properties
                existing = self._nodes[node.id]
                existing.properties.update(node.properties)
                existing.confidence = max(existing.confidence, node.confidence)
            else:
                self._nodes[node.id] = node
                count += 1
        return count

    def add_edges(self, edges: list[GraphEdge]) -> int:
        """Add edges to the graph, returning count added."""
        count = 0
        for edge in edges:
            if edge.id in self._edges:
                existing = self._edges[edge.id]
                existing.weight = max(existing.weight, edge.weight)
                existing.confidence = max(existing.confidence, edge.confidence)
            else:
                self._edges[edge.id] = edge
                self._adjacency[edge.source_id].append(edge.target_id)
                count += 1
        return count

    def resolve_entities(self, threshold: float | None = None) -> list[ResolvedEntity]:
        """Run entity resolution and store results."""
        resolution_threshold = threshold or self._resolver.confidence_threshold  # noqa: F841
        resolved = self._resolver.resolve_all(list(self._nodes.values()))
        self._resolved = {r.canonical_id: r for r in resolved}
        return resolved

    def extract_edges(self, context: dict[str, Any] | None = None) -> list[GraphEdge]:
        """Extract edges from current nodes and add them to the graph."""
        edges = self._extractor.extract_edges(list(self._nodes.values()), context)
        self.add_edges(edges)
        return edges

    def build_full_graph(
        self,
        nodes: list[GraphNode],
        context: dict[str, Any] | None = None,
    ) -> None:
        """Full pipeline: add nodes, resolve entities, extract edges."""
        self.add_nodes(nodes)
        self.resolve_entities()
        self.extract_edges(context)
        self._persist()

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def query_nodes(
        self,
        query: str | None = None,
        node_type: NodeType | None = None,
        domain: str | None = None,
        min_confidence: float = 0.0,
    ) -> list[GraphNode]:
        """Query nodes by various filters."""
        results: list[GraphNode] = []
        query_lower = (query or "").lower()

        for node in self._nodes.values():
            if node_type and node.node_type != node_type:
                continue
            if domain and node.domain != domain:
                continue
            if node.confidence < min_confidence:
                continue
            if query_lower:
                if (
                    query_lower not in node.name.lower()
                    and query_lower not in node.description.lower()
                ):  # noqa: E501
                    continue
            results.append(node)

        return results

    def get_related(
        self,
        node_id: str,
        relation: RelationType | None = None,
        max_depth: int = 3,
    ) -> list[GraphEdge]:
        """Get edges related to a node, optionally filtered by relation type."""
        results: list[GraphEdge] = []
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(node_id, 0)]

        while queue:
            current_id, depth = queue.pop(0)
            if current_id in visited or depth > max_depth:
                continue
            visited.add(current_id)

            for edge in self._edges.values():
                if edge.source_id == current_id or edge.target_id == current_id:
                    if relation is None or edge.relation == relation:
                        results.append(edge)
                        target = edge.target_id if edge.source_id == current_id else edge.source_id
                        queue.append((target, depth + 1))

        return results

    def find_path(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 5,
    ) -> list[list[GraphEdge]] | None:
        """Find paths between two nodes."""
        if start_id == end_id:
            return []

        paths: list[list[GraphEdge]] = []

        def dfs(current: str, path: list[GraphEdge], visited: set[str]) -> None:
            if len(path) >= max_depth:
                return
            if current == end_id:
                paths.append(list(path))
                return

            visited.add(current)
            for edge in self._edges.values():
                if edge.source_id == current and edge.target_id not in visited:
                    path.append(edge)
                    dfs(edge.target_id, path, visited)
                    path.pop()
                elif edge.target_id == current and edge.source_id not in visited:
                    path.append(edge)
                    dfs(edge.source_id, path, visited)
                    path.pop()
            visited.discard(current)

        dfs(start_id, [], set())
        return paths if paths else None

    def traverse(
        self,
        start_id: str,
        relation: RelationType | None = None,
        max_depth: int = 3,
    ) -> list[GraphNode]:
        """Traverse the graph from a starting node."""
        results: list[GraphNode] = []
        visited: set[str] = {start_id}
        queue: list[tuple[str, int]] = [(start_id, 0)]

        while queue:
            current_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self._edges.values():
                next_id = None
                if edge.source_id == current_id:
                    next_id = edge.target_id
                elif edge.target_id == current_id and relation is None:
                    next_id = edge.source_id

                if next_id and next_id not in visited:
                    if relation is None or edge.relation == relation:
                        node = self._nodes.get(next_id)
                        if node:
                            results.append(node)
                            visited.add(next_id)
                            queue.append((next_id, depth + 1))

        return results

    def get_node(self, node_id: str) -> GraphNode | None:
        """Get a single node by ID."""
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> GraphEdge | None:
        """Get a single edge by ID."""
        return self._edges.get(edge_id)

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def infer_answer(
        self,
        query: str,
        max_depth: int = 3,
        top_k: int = 5,
    ) -> InferenceResult:
        """
        Infer an answer to a cross-domain question using graph traversal.

        This is a deterministic graph-based inference. For LLM-enhanced
        inference, use the InferenceEngine.
        """
        query_lower = query.lower()

        # Find relevant nodes
        relevant_nodes = self.query_nodes(query=query_lower)[:top_k]

        if not relevant_nodes:
            return InferenceResult(
                answer=f"No relevant information found for: {query}",
                evidence_chain=[],
                source_entities=[],
                confidence=0.0,
            )

        # Build evidence chain from relationships
        evidence_chain: list[str] = []
        source_entities: list[str] = []

        for node in relevant_nodes:
            edges = self.get_related(node.id, max_depth=max_depth)
            source_entities.append(node.name)

            for edge in edges[:3]:  # Top 3 relationships per node
                target = self._nodes.get(edge.target_id)
                if target:
                    evidence_chain.append(
                        f"{node.name} {edge.relation.value} {target.name} "
                        f"(confidence: {edge.confidence:.2f})"
                    )

        # Synthesize answer
        answer_parts = []
        for i, node in enumerate(relevant_nodes):
            if i < 3:
                answer_parts.append(f"Found entity '{node.name}' in domain '{node.domain}'")

        if evidence_chain:
            answer_parts.append(f"Key relationships: {'; '.join(evidence_chain[:3])}")

        answer = ". ".join(answer_parts) if answer_parts else "No direct evidence found."

        confidence = min(1.0, sum(n.confidence for n in relevant_nodes) / len(relevant_nodes))

        return InferenceResult(
            answer=answer,
            evidence_chain=evidence_chain[:5],
            source_entities=source_entities,
            confidence=round(confidence, 4),
        )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _persist(self) -> None:
        """Persist graph to disk."""
        graph_data = {
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "node_type": n.node_type.value,
                    "domain": n.domain,
                    "layer": n.layer,
                    "description": n.description,
                    "properties": n.properties,
                    "confidence": n.confidence,
                }
                for n in self._nodes.values()
            ],
            "edges": [
                {
                    "id": e.id,
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation": e.relation.value,
                    "weight": e.weight,
                    "confidence": e.confidence,
                    "evidence": e.evidence,
                }
                for e in self._edges.values()
            ],
        }

        path = self.persist_path / "graph.json"
        path.write_text(json.dumps(graph_data, indent=2))

    def load(self) -> bool:
        """Load graph from disk."""
        path = self.persist_path / "graph.json"
        if not path.exists():
            return False

        data = json.loads(path.read_text())
        for node_data in data.get("nodes", []):
            node = GraphNode(
                id=node_data["id"],
                name=node_data["name"],
                node_type=NodeType(node_data["node_type"]),
                domain=node_data["domain"],
                layer=node_data["layer"],
                description=node_data.get("description", ""),
                properties=node_data.get("properties", {}),
                confidence=node_data.get("confidence", 0.5),
            )
            self._nodes[node.id] = node

        for edge_data in data.get("edges", []):
            edge = GraphEdge(
                id=edge_data["id"],
                source_id=edge_data["source_id"],
                target_id=edge_data["target_id"],
                relation=RelationType(edge_data["relation"]),
                weight=edge_data.get("weight", 1.0),
                confidence=edge_data.get("confidence", 0.5),
                evidence=edge_data.get("evidence", []),
            )
            self._edges[edge.id] = edge
            self._adjacency[edge.source_id].append(edge.target_id)

        return True

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict[str, Any]:
        """Return graph statistics."""
        domains = set(n.domain for n in self._nodes.values())
        node_types = set(n.node_type.value for n in self._nodes.values())

        return {
            "node_count": len(self._nodes),
            "edge_count": len(self._edges),
            "domains": list(domains),
            "node_types": list(node_types),
            "avg_confidence": round(
                sum(n.confidence for n in self._nodes.values()) / max(len(self._nodes), 1),
                4,
            ),
            "edges_by_relation": {
                rel: sum(1 for e in self._edges.values() if e.relation.value == rel)
                for rel in set(e.relation.value for e in self._edges.values())
            },
        }
