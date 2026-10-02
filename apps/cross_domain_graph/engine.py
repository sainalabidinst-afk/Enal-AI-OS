"""
Cross-Domain Knowledge Graph Engine — domain engine orchestrator.

Orchestrates the full cross-domain knowledge graph pipeline:
    1. MemoryScanner (scan all memory layers for entities)
    2. EntityResolver (identify same entity across domains)
    3. EdgeExtractor (discover relationships between entities)
    4. GraphBuilder (build and maintain the persistent graph)
    5. InferenceEngine (answer cross-domain questions)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.cross_domain_graph.edge_extractor import EdgeExtractor
from apps.cross_domain_graph.entity_resolver import EntityResolver
from apps.cross_domain_graph.graph_builder import GraphBuilder
from apps.cross_domain_graph.memory_scanner import MemoryScanner
from apps.cross_domain_graph.schemas import (
    GraphQueryRequest,
    GraphQueryResult,
    InferenceResult,
)

logger = logging.getLogger(__name__)


class CrossDomainGraphEngine:
    """
    Orchestrates the full cross-domain knowledge graph pipeline.

    Public API::

        engine = CrossDomainGraphEngine()
        result = await engine.query("What correlates with interest rates?")
        engine.build_graph()
    """

    def __init__(self, persist_path: str = "./workspace/cross_domain_graph") -> None:
        self.resolver = EntityResolver()
        self.extractor = EdgeExtractor(self.resolver)
        self.builder = GraphBuilder(persist_path=persist_path, resolver=self.resolver, extractor=self.extractor)  # noqa: E501
        self.scanner = MemoryScanner()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def build_graph(
        self,
        query: str | None = None,
        layers: list[str] | None = None,
        limit_per_layer: int = 100,
        project_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build/update the cross-domain knowledge graph by scanning memory layers.

        Args:
            query: Optional search query to guide scanning.
            layers: Specific layers to scan (default: all).
            limit_per_layer: Max entries per layer.
            project_id: Optional project scoping.
            context: Additional context for edge extraction.

        Returns:
            Summary of the graph build operation.
        """
        started = time.monotonic()

        # Step 1: Scan memory layers
        nodes = await self.scanner.scan_all(
            layers=layers,
            query=query,
            limit_per_layer=limit_per_layer,
            project_id=project_id,
        )
        logger.info(f"Memory scan: {len(nodes)} nodes from layers")

        # Step 2: Build full graph
        self.builder.build_full_graph(nodes, context)

        # Step 3: Return stats
        stats = self.builder.stats()
        stats["scan_time_ms"] = round((time.monotonic() - started) * 1000, 2)
        stats["nodes_scanned"] = len(nodes)

        return stats

    async def query(
        self,
        request: GraphQueryRequest | str,
    ) -> GraphQueryResult:
        """
        Query the cross-domain knowledge graph.

        Args:
            request: GraphQueryRequest or a simple query string.

        Returns:
            GraphQueryResult with answer, entities, and relationships.
        """
        started = time.monotonic()

        if isinstance(request, str):
            from apps.cross_domain_graph.schemas import GraphQueryRequest as _Req
            request = _Req(query=request)

        # Ensure graph has been loaded or built
        if not self.builder._nodes:
            await self.build_graph(query=request.query, context={"query": request.query})

        # Extract subgraphs relevant to the query
        relevant_nodes = self.builder.query_nodes(query=request.query)[:20]
        relevant_node_ids = [n.id for n in relevant_nodes]

        # Get edges between relevant nodes
        edges = self._get_subgraph_edges(relevant_node_ids)

        # Run inference
        inference = await self._run_inference(request, relevant_nodes)

        # Find relationship paths between top entities
        relationship_paths = []
        if len(relevant_nodes) >= 2:
            for i in range(min(3, len(relevant_nodes) - 1)):
                paths = self.builder.find_path(
                    relevant_nodes[i].id,
                    relevant_nodes[i + 1].id,
                    max_depth=request.max_depth,
                )
                if paths:
                    for path in paths[:1]:
                        relationship_paths.append([e.id for e in path])

        graph_snapshot = {
            "node_count": len(relevant_nodes),
            "edge_count": len(edges),
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "domain": n.domain,
                    "layer": n.layer,
                    "node_type": n.node_type.value,
                    "confidence": n.confidence,
                }
                for n in relevant_nodes
            ],
            "edges": [
                {
                    "id": e.id,
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation": e.relation.value,
                    "weight": e.weight,
                    "confidence": e.confidence,
                }
                for e in edges
            ],
        }

        result = GraphQueryResult(
            request_id=request.request_id,
            query=request.query,
            answer=inference.answer if inference else "No inference available.",
            entities_discovered=[
                {"id": n.id, "name": n.name, "domain": n.domain, "layer": n.layer, "confidence": n.confidence}  # noqa: E501
                for n in relevant_nodes
            ],
            relationships=[
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "relation": e.relation.value,
                    "confidence": e.confidence,
                }
                for e in edges
            ],
            relationship_paths=relationship_paths,
            inference=inference,
            confidence=inference.confidence if inference else 0.0,
            graph_snapshot=graph_snapshot,
            explanation=self._build_explanation(request, relevant_nodes, edges, inference),
            raw={
                "query_time_ms": round((time.monotonic() - started) * 1000, 2),
                "nodes_searched": len(self.builder._nodes),
            },
        )

        return result

    def explain_relationship(
        self,
        source_entity: str,
        target_entity: str,
        max_depth: int = 5,
    ) -> dict[str, Any]:
        """Explain how two entities are related in the graph."""
        source_nodes = self.builder.query_nodes(query=source_entity)
        target_nodes = self.builder.query_nodes(query=target_entity)

        if not source_nodes or not target_nodes:
            return {
                "explanation": f"Could not find entities: '{source_entity}' or '{target_entity}'",
                "paths": [],
            }

        paths = self.builder.find_path(source_nodes[0].id, target_nodes[0].id, max_depth=max_depth)

        if not paths:
            return {
                "explanation": f"No path found between '{source_entity}' and '{target_entity}'",
                "paths": [],
            }

        path_explanations = []
        for path in paths[:3]:
            explanation_parts = []
            for edge in path:
                src = self.builder.get_node(edge.source_id)
                tgt = self.builder.get_node(edge.target_id)
                if src and tgt:
                    explanation_parts.append(
                        f"{src.name} --{edge.relation.value}--> {tgt.name}"
                    )
            path_explanations.append(" | ".join(explanation_parts))

        return {
            "explanation": f"Found {len(paths)} path(s) between '{source_entity}' and '{target_entity}'",  # noqa: E501
            "paths": path_explanations,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_subgraph_edges(self, node_ids: list[str]) -> list[Any]:
        """Get edges where both endpoints are in the given node set."""
        edges: list[Any] = []
        node_set = set(node_ids)

        for edge in self.builder._edges.values():
            if edge.source_id in node_set and edge.target_id in node_set:
                edges.append(edge)

        return edges

    async def _run_inference(
        self,
        request: GraphQueryRequest,
        relevant_nodes: list[Any],
    ) -> InferenceResult | None:
        """Run inference to answer the query."""
        # First try deterministic graph-based inference
        deterministic = self.builder.infer_answer(
            request.query,
            max_depth=request.max_depth,
            top_k=min(5, len(relevant_nodes)),
        )

        # If we have LLM inference available, enhance with LLM
        try:
            from backend.app.runtime import settings

            has_llm = any(
                [
                    settings.OPENAI_API_KEY,
                    settings.ANTHROPIC_API_KEY,
                    settings.GOOGLE_API_KEY,
                    settings.GEMINI_API_KEY,
                ]
            )
            if not has_llm:
                logger.debug("No LLM API keys configured, using deterministic inference")
                return deterministic

            import asyncio

            llm_result = await asyncio.wait_for(
                self._llm_inference(request, relevant_nodes, deterministic),
                timeout=5.0,
            )
            return llm_result
        except TimeoutError as e:
            logger.debug(f"LLM inference timed out, using deterministic: {e}")
            return deterministic
        except Exception as e:
            logger.debug(f"LLM inference not available, using deterministic: {e}")
            return deterministic

    async def _llm_inference(
        self,
        request: GraphQueryRequest,
        relevant_nodes: list[Any],
        fallback: InferenceResult,
    ) -> InferenceResult:
        """Enhance inference using LLM for natural language synthesis."""
        from backend.app.runtime import settings
        from backend.app.runtime import model_router

        node_descs = [
            f"{n.name} (domain: {n.domain}, layer: {n.layer}): {n.description}"
            for n in relevant_nodes[:10]
        ]
        context = "\n".join(node_descs)

        prompt = (
            f"Answer the following cross-domain question based on the provided entities.\n\n"
            f"Question: {request.query}\n\n"
            f"Relevant entities:\n{context}\n\n"
            f"Fallback answer: {fallback.answer}\n\n"
            "Output JSON: {\"answer\": str, \"confidence\": float}"
        )

        response = await model_router.acomplete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )

        import json
        try:
            data = json.loads(response.choices[0].message.content)
            return InferenceResult(
                answer=data.get("answer", fallback.answer),
                evidence_chain=fallback.evidence_chain,
                source_entities=fallback.source_entities,
                confidence=min(1.0, data.get("confidence", fallback.confidence)),
            )
        except (json.JSONDecodeError, AttributeError):
            return fallback

    def _build_explanation(
        self,
        request: GraphQueryRequest,
        nodes: list[Any],
        edges: list[Any],
        inference: InferenceResult | None,
    ) -> dict[str, Any]:
        """Build the explanation chain for the query result."""
        return {
            "reasoning_chain": [
                f"Query: {request.query}",
                f"Found {len(nodes)} relevant entities across domains: "
                f"{', '.join(set(n.domain for n in nodes))}",
                f"Discovered {len(edges)} relationships",
                f"Inference confidence: {inference.confidence if inference else 0.0}",
            ],
            "evidence_sources": [
                {"entity_id": n.id, "name": n.name, "domain": n.domain, "layer": n.layer}
                for n in nodes[:5]
            ],
            "graph_stats": self.builder.stats(),
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load_graph(self) -> bool:
        """Load persisted graph from disk."""
        return self.builder.load()
