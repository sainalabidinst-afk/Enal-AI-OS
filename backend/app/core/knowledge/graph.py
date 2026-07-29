from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from backend.app.core.knowledge.edge import KnowledgeEdge, RelationType
from backend.app.core.knowledge.node import KnowledgeNode


@dataclass
class KnowledgeGraph:
    nodes: dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: dict[str, KnowledgeEdge] = field(default_factory=dict)
    _adjacency: dict[str, list[str]] = field(default_factory=dict)

    def add_node(self, node: KnowledgeNode) -> KnowledgeNode:
        self.nodes[node.id] = node
        self._adjacency.setdefault(node.id, [])
        return node

    def add_edge(self, edge: KnowledgeEdge) -> KnowledgeEdge:
        self.edges[edge.id] = edge
        self._adjacency.setdefault(edge.source_id, []).append(edge.target_id)
        return edge

    def get_node(self, node_id: str) -> KnowledgeNode | None:
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: str) -> KnowledgeEdge | None:
        return self.edges.get(edge_id)

    def neighbors(self, node_id: str) -> list[KnowledgeNode]:
        neighbor_ids = self._adjacency.get(node_id, [])
        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]

    def relations(self, source_id: str, relation: str | None = None) -> list[KnowledgeEdge]:
        result = []
        for edge in self.edges.values():
            if edge.source_id == source_id and (relation is None or edge.relation == relation):
                result.append(edge)
        return result

    def path(self, start_id: str, end_id: str, max_depth: int = 5) -> list[list[KnowledgeEdge]] | None:
        visited = set()
        paths: list[list[KnowledgeEdge]] = []

        def dfs(current: str, path: list[KnowledgeEdge]) -> None:
            if current == end_id:
                paths.append(list(path))
                return
            if len(path) >= max_depth:
                return
            visited.add(current)
            for edge in self.edges.values():
                if edge.source_id == current and edge.target_id not in visited:
                    path.append(edge)
                    dfs(edge.target_id, path)
                    path.pop()
            visited.discard(current)

        dfs(start_id, [])
        return paths if paths else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [
                {
                    "id": n.id,
                    "domain": n.domain,
                    "category": n.category,
                    "type": n.type,
                    "name": n.name,
                    "description": n.description,
                    "status": n.status,
                    "confidence": n.confidence,
                    "tags": n.tags,
                    "metadata": n.metadata,
                    "related_ids": n.related_ids,
                    "source": n.source,
                    "owner": n.owner,
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "id": e.id,
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation": e.relation,
                    "weight": e.weight,
                    "confidence": e.confidence,
                    "metadata": e.metadata,
                }
                for e in self.edges.values()
            ],
        }
