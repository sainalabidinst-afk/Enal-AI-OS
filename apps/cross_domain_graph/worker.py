"""
Cross-Domain Knowledge Graph Worker — thin adapter (per ADR-003).

Routes task requests to the Cross-Domain Knowledge Graph Domain Engine.
"""

from __future__ import annotations

from typing import Any

from apps.cross_domain_graph.engine import CrossDomainGraphEngine
from apps.cross_domain_graph.schemas import GraphQueryRequest


class CrossDomainGraphWorker:
    """
    Thin Worker adapter for the Cross-Domain Knowledge Graph Capability Pack.

    Responsibilities:
        - Parse incoming task into GraphQueryRequest
        - Delegate to CrossDomainGraphEngine
        - Return result as dict
    """

    def __init__(self, engine: CrossDomainGraphEngine | None = None) -> None:
        self._engine = engine or CrossDomainGraphEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a cross-domain graph query task.

        Expected task format::

            {
                "query": "What correlates with interest rates?",
                "source_domains": ["trading", "macro"],
                "target_memory_layers": ["knowledge", "episodic"],
                "max_depth": 3,
                "include_explanations": true,
                "confidence_threshold": 0.5,
            }

        Returns:
            GraphQueryResult as a JSON-serializable dict.
        """
        request = GraphQueryRequest(
            query=task.get("query", ""),
            source_domains=task.get("source_domains", []),
            target_memory_layers=task.get(
                "target_memory_layers", ["knowledge", "episodic", "project", "longterm"]
            ),
            max_depth=task.get("max_depth", 3),
            include_explanations=task.get("include_explanations", True),
            confidence_threshold=task.get("confidence_threshold", 0.5),
        )

        result = await self._engine.query(request)
        return result.to_dict()

    async def build(self, task: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build/update the cross-domain graph."""
        task = task or {}
        stats = await self._engine.build_graph(
            query=task.get("query"),
            layers=task.get("layers"),
            limit_per_layer=task.get("limit_per_layer", 100),
            project_id=task.get("project_id"),
            context=task.get("context"),
        )
        return stats

    def explain(self, source: str, target: str, max_depth: int = 5) -> dict[str, Any]:
        """Explain how two entities are related."""
        return self._engine.explain_relationship(source, target, max_depth=max_depth)

    def stats(self) -> dict[str, Any]:
        """Return graph statistics."""
        return self._engine.builder.stats()

    def load(self) -> bool:
        """Load persisted graph."""
        return self._engine.load_graph()
