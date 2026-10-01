"""
Cross-Domain Knowledge Graph — The "Connector".

Capability Pack that automatically scans all Memory layers and maps
entity relationships across domains, transforming ECP from a retrieval
system into a cross-domain connection system.

Pipeline:
    GraphQueryRequest
        ↓
    MemoryScanner (scan all 7 memory layers for entities)
        ↓
    EntityResolver (identify same entity across domains/layers)
        ↓
    EdgeExtractor (discover relationships between entities)
        ↓
    GraphBuilder (build and maintain persistent graph)
        ↓
    InferenceEngine (cross-domain Q&A with explanation)
        ↓
    GraphQueryResult
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.cross_domain_graph.engine import CrossDomainGraphEngine
from apps.cross_domain_graph.schemas import (
    GraphEdge,
    GraphNode,
    GraphQueryRequest,
    GraphQueryResult,
    InferenceResult,
    NodeType,
    RelationType,
    ResolvedEntity,
)
from apps.cross_domain_graph.worker import CrossDomainGraphWorker


class CrossDomainGraphApp(BaseReferenceApp):
    name = "cross-domain-graph"
    version = "1.0.0"
    description = "Automatic cross-domain entity relationship mapping and inference"
    category = "knowledge"
    pipeline = ["perception", "memory", "reasoning", "decision"]

    def __init__(self) -> None:
        self.worker = CrossDomainGraphWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("query", user_input)
        return await self.worker.execute(task)


def get_app() -> CrossDomainGraphApp:
    return CrossDomainGraphApp()


__all__ = [
    "CrossDomainGraphApp",
    "get_app",
    "CrossDomainGraphEngine",
    "CrossDomainGraphWorker",
    "GraphQueryRequest",
    "GraphQueryResult",
    "InferenceResult",
    "GraphNode",
    "GraphEdge",
    "ResolvedEntity",
    "NodeType",
    "RelationType",
]
