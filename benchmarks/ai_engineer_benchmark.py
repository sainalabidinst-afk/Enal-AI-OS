"""
AI Engineer Benchmark
=====================

Benchmark scenarios for validating AI Engineer capability pack.
Target: A+ (≥95%) with 10 scenarios across 6 dimensions.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "ai-001",
        "name": "RAG Chatbot untuk Knowledge Base",
        "category": "rag",
        "inputs": {
            "business_context": {"project_name": "kb-chatbot", "domain": "customer-support"},
            "inputs": {"rag_strategy": "hybrid", "top_k": 5, "chunk_size": 512},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-002",
        "name": "Multi-Agent Orchestration",
        "category": "agent_architecture",
        "inputs": {
            "business_context": {"project_name": "multi-agent", "domain": "research"},
            "inputs": {"agent_type": "hierarchical", "agent_count": 3},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-003",
        "name": "Prompt Engineering untuk Code Generation",
        "category": "prompt_engineering",
        "inputs": {
            "business_context": {"project_name": "code-gen", "domain": "software-development"},
            "inputs": {"template_type": "code_generation", "language": "python"},
        },
        "min_quality_score": 0.95,
    },
    {
        "id": "ai-004",
        "name": "LLMOps Deployment Pipeline",
        "category": "llmops",
        "inputs": {
            "business_context": {"project_name": "llmops-pipeline", "domain": "ml-platform"},
            "inputs": {"environment": "production", "scaling_min": 2, "gpu_enabled": True},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-005",
        "name": "Fine-Tuning untuk Domain-Specific LLM",
        "category": "fine_tuning",
        "inputs": {
            "business_context": {"project_name": "domain-llm", "domain": "legal"},
            "inputs": {"base_model": "llama-3-8b", "epochs": 3, "batch_size": 8},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-006",
        "name": "AI Evaluation Framework",
        "category": "evaluation",
        "inputs": {
            "business_context": {"project_name": "ai-eval", "domain": "ml-platform"},
            "inputs": {"metrics": ["accuracy", "f1", "latency"], "test_cases_count": 100},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-007",
        "name": "Guardrails untuk LLM Safety",
        "category": "guardrails",
        "inputs": {
            "business_context": {"project_name": "llm-guardrails", "domain": "customer-support"},
            "inputs": {"guardrail_types": ["content_filter", "pii_detection", "toxicity"]},
        },
        "min_quality_score": 0.95,
    },
    {
        "id": "ai-008",
        "name": "AI Observability Setup",
        "category": "observability",
        "inputs": {
            "business_context": {"project_name": "ai-observability", "domain": "ml-platform"},
            "inputs": {"metrics": ["latency", "token_usage", "drift"], "alert_threshold": "p95 > 2000ms"},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-009",
        "name": "Graph RAG untuk Enterprise Knowledge",
        "category": "rag",
        "inputs": {
            "business_context": {"project_name": "graph-rag", "domain": "enterprise"},
            "inputs": {"rag_strategy": "graph", "entity_types": ["person", "org", "document"]},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "ai-010",
        "name": "Agent Pipeline untuk Automated Research",
        "category": "agent_architecture",
        "inputs": {
            "business_context": {"project_name": "research-pipeline", "domain": "research"},
            "inputs": {"agent_type": "pipeline", "steps": ["search", "filter", "summarize", "synthesize"]},
        },
        "min_quality_score": 0.90,
    },
]


def get_scenarios() -> list[dict[str, Any]]:
    return SCENARIOS


def get_scenario_by_id(scenario_id: str) -> dict[str, Any] | None:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None
