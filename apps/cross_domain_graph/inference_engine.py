"""
Cross-Domain Knowledge Graph — Inference Engine.

Provides cross-domain Q&A with explanation, wrapping the graph traversal
and optional LLM synthesis from CrossDomainGraphEngine._run_inference.
"""

from __future__ import annotations

import logging

from apps.cross_domain_graph.graph_builder import GraphBuilder
from apps.cross_domain_graph.schemas import (
    GraphNode,
    GraphQueryRequest,
    InferenceResult,
)

logger = logging.getLogger(__name__)


class InferenceEngine:
    """Executes cross-domain inference by traversing the knowledge graph.

    Delegates to deterministic graph traversal first; enhances with LLM
    synthesis when an API key is available.
    """

    def __init__(self, graph_builder: GraphBuilder) -> None:
        self.builder = graph_builder

    def infer_answer(
        self,
        query: str,
        relevant_nodes: list[GraphNode],
        max_depth: int = 5,
        top_k: int = 5,
    ) -> InferenceResult:
        """Produce a deterministic inference result from the graph.

        Args:
            query: The user's cross-domain question.
            relevant_nodes: Nodes already identified as relevant.
            max_depth: Maximum path depth for traversal.
            top_k: Number of top edges to consider.

        Returns:
            InferenceResult with answer, evidence chain, and confidence.
        """
        evidence_chain: list[str] = []
        source_entities: list[str] = []

        for node in relevant_nodes[:top_k]:
            evidence_chain.append(
                f"Entity: {node.name} (domain={node.domain}, layer={node.layer})"
            )
            source_entities.append(node.id)

        paths = []
        for i in range(min(len(relevant_nodes) - 1, top_k)):
            src = relevant_nodes[i].id
            tgt = relevant_nodes[i + 1].id
            found_paths = self.builder.find_path(src, tgt, max_depth=max_depth)
            if found_paths:
                paths.extend(found_paths[:1])

        if paths:
            for path in paths[:3]:
                for edge in path:
                    src_node = self.builder.get_node(edge.source_id)
                    tgt_node = self.builder.get_node(edge.target_id)
                    if src_node and tgt_node:
                        evidence_chain.append(
                            f"Relationship: {src_node.name} {edge.relation.value} {tgt_node.name}"
                        )
                evidence_chain.append("Path traversed for inference")
            answer = (
                f"Based on cross-domain analysis, the answer relates to "
                f"{len(relevant_nodes)} entities and {len(paths)} relationship path(s)."
            )
            confidence = min(1.0, 0.7 + 0.05 * len(relevant_nodes))
        elif relevant_nodes:
            answer = (
                f"Query relates to {len(relevant_nodes)} entities across domains: "
                f"{', '.join(set(n.domain for n in relevant_nodes))}."
            )
            confidence = 0.5 + 0.05 * min(len(relevant_nodes), 5)
        else:
            answer = "Insufficient cross-domain data to form inference."
            confidence = 0.0

        return InferenceResult(
            answer=answer,
            evidence_chain=list(evidence_chain) if evidence_chain else ["No evidence"],
            source_entities=source_entities,
            confidence=confidence,
        )

    async def infer_async(
        self,
        request: GraphQueryRequest,
        relevant_nodes: list[GraphNode],
        max_depth: int = 5,
    ) -> InferenceResult:
        """Async wrapper that falls back to LLM enhancement when available."""
        deterministic = self.infer_answer(
            request.query, relevant_nodes, max_depth=max_depth, top_k=min(5, len(relevant_nodes))
        )

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
                return deterministic

            import asyncio
            import json

            node_descs = [
                f"{n.name} (domain: {n.domain}, layer: {n.layer}): {n.description}"
                for n in relevant_nodes[:10]
            ]
            context = "\n".join(node_descs)

            from backend.app.runtime import model_router

            prompt = (
                f"Answer cross-domain question: {request.query}\n"
                f"Relevant entities:\n{context}\n"
                f"Fallback: {deterministic.answer}\n"
                f"Output JSON: {{'answer': str, 'confidence': float}}"
            )

            response = await asyncio.wait_for(
                model_router.acomplete(
                    [{"role": "user", "content": prompt}],
                    model=settings.DEFAULT_REASONING_MODEL,
                    temperature=0.3,
                    max_tokens=1024,
                ),
                timeout=5.0,
            )
            data = json.loads(response.choices[0].message.content)
            return InferenceResult(
                answer=data.get("answer", deterministic.answer),
                evidence_chain=deterministic.evidence_chain,
                source_entities=deterministic.source_entities,
                confidence=min(1.0, data.get("confidence", deterministic.confidence)),
            )
        except Exception as e:
            logger.debug(f"LLM inference not available, using deterministic: {e}")
            return deterministic
