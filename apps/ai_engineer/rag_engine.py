"""
RAG Engine
==========

Designs retrieval-augmented generation configurations:
chunking strategies, embedding models, vector stores, and reranking.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ai_engineer.schemas import (
    AIEngineerRequest,
    RAGConfig,
    RAGStrategy,
    EvaluationMetric,
)

logger = logging.getLogger(__name__)

CHUNK_SIZE_MAP: dict[str, int] = {
    "naive": 0,
    "chunked": 512,
    "hybrid": 512,
    "graph": 1024,
    "agentic": 2048,
}

TOP_K_DEFAULT: dict[str, int] = {
    "naive": 3,
    "chunked": 5,
    "hybrid": 7,
    "graph": 10,
    "agentic": 15,
}


class RAGEngine:
    """Designs RAG engine configurations."""

    def design(self, request: AIEngineerRequest) -> RAGConfig:
        inputs = request.inputs
        strategy_value = inputs.get("strategy", "chunked")
        try:
            strategy = RAGStrategy(strategy_value)
        except ValueError:
            strategy = RAGStrategy.chunked

        chunk_size = inputs.get("chunk_size", CHUNK_SIZE_MAP.get(strategy_value, 512))
        chunk_overlap = inputs.get("chunk_overlap", 50 if chunk_size > 0 else 0)
        top_k = inputs.get("top_k", TOP_K_DEFAULT.get(strategy_value, 5))

        rerank = inputs.get("rerank_enabled", strategy in (RAGStrategy.hybrid, RAGStrategy.agentic))
        rerank_model = inputs.get("rerank_model", "cohere-rerank-v3" if rerank else "")

        return RAGConfig(
            strategy=strategy,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_model=inputs.get("embedding_model", "text-embedding-3-small"),
            vector_store=inputs.get("vector_store", "pinecone"),
            top_k=top_k,
            rerank_enabled=rerank,
            rerank_model=rerank_model,
        )

    def get_recommendations(self, config: RAGConfig) -> list[str]:
        recs: list[str] = []
        if config.chunk_size == 0:
            recs.append("Pertimbangkan chunking strategy untuk dokumen panjang")
        if config.chunk_overlap < config.chunk_size * 0.1:
            recs.append("Tingkatkan chunk overlap untuk menjaga konteks lintas chunk")
        if not config.rerank_enabled and config.top_k > 5:
            recs.append("Aktifkan reranking untuk top_k > 5")
        if config.vector_store == "local" and config.strategy == RAGStrategy.agentic:
            recs.append("Pertimbangkan vector store terdistribusi untuk agentic RAG")
        return recs

    def estimate_cost(self, config: RAGConfig) -> dict[str, float]:
        embedding_cost_per_1k = 0.00002
        monthly_embeddings = 10_000_000
        rerank_cost_per_1k = 0.001 if config.rerank_enabled else 0.0
        vector_store_cost = 25.0 if config.vector_store == "pinecone" else 0.0

        monthly = (monthly_embeddings / 1000) * embedding_cost_per_1k
        monthly += vector_store_cost
        monthly += (monthly_embeddings / 1000) * rerank_cost_per_1k * config.top_k

        return {
            "embedding_monthly": round((monthly_embeddings / 1000) * embedding_cost_per_1k, 2),
            "rerank_monthly": round((monthly_embeddings / 1000) * rerank_cost_per_1k * config.top_k, 2),
            "vector_store_monthly": vector_store_cost,
            "total_monthly": round(monthly, 2),
        }

    def evaluate(self, config: RAGConfig) -> dict[str, float]:
        scores = {
            RAGStrategy.naive: {"faithfulness": 0.75, "hallucination_rate": 0.15},
            RAGStrategy.chunked: {"faithfulness": 0.88, "hallucination_rate": 0.08},
            RAGStrategy.hybrid: {"faithfulness": 0.92, "hallucination_rate": 0.05},
            RAGStrategy.graph: {"faithfulness": 0.90, "hallucination_rate": 0.06},
            RAGStrategy.agentic: {"faithfulness": 0.94, "hallucination_rate": 0.03},
        }
        return scores.get(config.strategy, {"faithfulness": 0.85, "hallucination_rate": 0.08})

    def score_quality(self, config: RAGConfig) -> float:
        base = {
            RAGStrategy.naive: 0.7,
            RAGStrategy.chunked: 0.8,
            RAGStrategy.hybrid: 0.88,
            RAGStrategy.graph: 0.85,
            RAGStrategy.agentic: 0.9,
        }
        score = base.get(config.strategy, 0.8)
        if config.rerank_enabled:
            score += 0.05
        return min(score, 1.0)
