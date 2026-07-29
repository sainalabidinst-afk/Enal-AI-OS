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

    def query(self, **filters: Any) -> list[KnowledgeNode]:
        results = list(self.nodes.values())
        if "domain" in filters:
            results = [n for n in results if n.domain == filters["domain"]]
        if "category" in filters:
            results = [n for n in results if n.category == filters["category"]]
        if "type" in filters:
            results = [n for n in results if n.type == filters["type"]]
        if "status" in filters:
            results = [n for n in results if n.status == filters["status"]]
        if "tag" in filters:
            results = [n for n in results if filters["tag"] in n.tags]
        if "name_contains" in filters:
            lowered = filters["name_contains"].lower()
            results = [n for n in results if lowered in n.name.lower()]
        if "min_confidence" in filters:
            results = [n for n in results if n.confidence >= filters["min_confidence"]]
        if "related_to" in filters:
            related_ids = {e.target_id for e in self.edges.values() if e.source_id == filters["related_to"]}
            results = [n for n in results if n.id in related_ids]
        return results

    def similarity(self, query: str, limit: int = 5) -> list[tuple[KnowledgeNode, float]]:
        query_terms = set(query.lower().split())
        scored: list[tuple[KnowledgeNode, float]] = []
        for node in self.nodes.values():
            text = " ".join([node.name, node.description, " ".join(node.tags)]).lower()
            node_terms = set(text.split())
            overlap = query_terms & node_terms
            score = len(overlap) / max(len(query_terms), 1)
            if score > 0:
                scored.append((node, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]

    def traverse(self, start_id: str, relation: str | None = None, max_depth: int = 3) -> list[list[KnowledgeNode]]:
        paths: list[list[KnowledgeNode]] = []

        def dfs(current_id: str, current_path: list[KnowledgeNode], depth: int) -> None:
            if depth >= max_depth:
                return
            current_node = self.nodes.get(current_id)
            if not current_node:
                return
            current_path = current_path + [current_node]
            for edge in self.edges.values():
                if edge.source_id == current_id and (relation is None or edge.relation == relation):
                    target = self.nodes.get(edge.target_id)
                    if target:
                        paths.append(current_path + [target])
                        dfs(edge.target_id, current_path + [target], depth + 1)

        dfs(start_id, [], 0)
        return paths

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
