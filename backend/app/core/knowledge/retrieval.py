from __future__ import annotations

from typing import Any
from backend.app.core.knowledge.graph import KnowledgeGraph, KnowledgeNode
from backend.app.core.knowledge.registry import KnowledgeRegistry


class KnowledgeRetrieval:
    def __init__(self, registry: KnowledgeRegistry, graph: KnowledgeGraph) -> None:
        self.registry = registry
        self.graph = graph

    def search(self, query: str, domain: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        candidates = self.graph.similarity(query, limit=limit * 2)
        if domain:
            candidates = [(node, score) for node, score in candidates if node.domain == domain]
        results = []
        for node, score in candidates[:limit]:
            entity = self.registry.resolve(node.id)
            results.append({
                "id": node.id,
                "name": node.name,
                "description": node.description,
                "domain": node.domain,
                "category": node.category,
                "type": node.type,
                "confidence": node.confidence,
                "score": score,
                "entity": entity,
            })
        return results

    def related(self, concept_id: str, relation: str | None = None, max_depth: int = 2) -> list[dict[str, Any]]:
        paths = self.graph.traverse(concept_id, relation=relation, max_depth=max_depth)
        results: list[dict[str, Any]] = []
        seen: set[str] = set()
        for path in paths:
            for node in path:
                if node.id not in seen:
                    seen.add(node.id)
                    results.append({
                        "id": node.id,
                        "name": node.name,
                        "description": node.description,
                        "domain": node.domain,
                        "category": node.category,
                        "type": node.type,
                    })
        return results

    def hybrid(self, query: str, domain: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        graph_results = self.search(query, domain=domain, limit=limit)
        registry_results = self.registry.find_by_name(query)
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
