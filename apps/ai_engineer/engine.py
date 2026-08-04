"""
AI Engineer — Domain Engine orchestrator.

Orchestrates the full AI engineering pipeline:
    1. Agent Design — Agent architecture and tool specification
    2. RAG Engine Design — Retrieval-augmented generation configuration
    3. Prompt Engineering — Prompt template design and optimization
    4. LLMOps Setup — Deployment, monitoring, and evaluation
    5. AI Assessment — Gap analysis and improvement recommendations

All AI engineering logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ai_engineer.agent_designer import AgentDesigner
from apps.ai_engineer.rag_engine import RAGEngine
from apps.ai_engineer.prompt_engineer import PromptEngineer
from apps.ai_engineer.llmops_manager import LLMOpsManager
from apps.ai_engineer.schemas import (
    AIEngineerRequest,
    AIEngineerReport,
)

logger = logging.getLogger(__name__)


class AIEngineerEngine:
    """
    Orchestrates the full AI engineering pipeline.

    Public API::

        engine = AIEngineerEngine()
        report = engine.design(request)
    """

    def __init__(self) -> None:
        self.agent_designer = AgentDesigner()
        self.rag_engine = RAGEngine()
        self.prompt_engineer = PromptEngineer()
        self.llmops_manager = LLMOpsManager()

    def design(self, request: AIEngineerRequest) -> AIEngineerReport:
        """
        Run the AI engineering pipeline based on operation.

        Args:
            request: AIEngineerRequest with context, inputs, options.

        Returns:
            AIEngineerReport with all generated artifacts.
        """
        op = request.operation
        logger.info("Running AI engineering operation: %s", op.value)

        agent_spec = None
        rag_config = None
        prompt_templates: list[Any] = []
        fine_tuning_config = None
        deployment_config = None
        monitoring_config = None
        evaluation_results: dict[str, float] = {}
        recommendations: list[str] = []
        cost_estimate: dict[str, float] = {}
        quality_score = 0.85

        if op == AIEngineerRequest.operation.agent_design:
            agent_spec = self.agent_designer.design_agent(request)
            recommendations = self.agent_designer.get_recommendations(agent_spec)
            cost_estimate = self.agent_designer.estimate_cost(agent_spec)
            evaluation_results = self.agent_designer.evaluate(agent_spec)
            quality_score = self.agent_designer.score_quality(agent_spec)

        elif op == AIEngineerRequest.operation.rag_engine_design:
            rag_config = self.rag_engine.design(request)
            recommendations = self.rag_engine.get_recommendations(rag_config)
            cost_estimate = self.rag_engine.estimate_cost(rag_config)
            evaluation_results = self.rag_engine.evaluate(rag_config)
            quality_score = self.rag_engine.score_quality(rag_config)

        elif op == AIEngineerRequest.operation.prompt_engineering:
            prompt_templates = self.prompt_engineer.design(request)
            recommendations = self.prompt_engineer.get_recommendations(prompt_templates)
            quality_score = self.prompt_engineer.score_quality(prompt_templates)

        elif op == AIEngineerRequest.operation.llmops_setup:
            deployment_config = self.llmops_manager.design_deployment(request)
            monitoring_config = self.llmops_manager.design_monitoring(request)
            fine_tuning_config = self.llmops_manager.design_fine_tuning(request)
            recommendations = self.llmops_manager.get_recommendations(deployment_config, monitoring_config)
            cost_estimate = self.llmops_manager.estimate_cost(deployment_config, fine_tuning_config)
            quality_score = self.llmops_manager.score_quality(deployment_config, monitoring_config)

        elif op == AIEngineerRequest.operation.ai_assessment:
            agent_spec = self.agent_designer.design_agent(request)
            rag_config = self.rag_engine.design(request)
            prompt_templates = self.prompt_engineer.design(request)
            deployment_config = self.llmops_manager.design_deployment(request)
            monitoring_config = self.llmops_manager.design_monitoring(request)
            recommendations = (
                self.agent_designer.get_recommendations(agent_spec)
                + self.rag_engine.get_recommendations(rag_config)
                + self.prompt_engineer.get_recommendations(prompt_templates)
                + self.llmops_manager.get_recommendations(deployment_config, monitoring_config)
            )
            cost_estimate = self._aggregate_costs(
                self.agent_designer.estimate_cost(agent_spec),
                self.rag_engine.estimate_cost(rag_config),
                self.llmops_manager.estimate_cost(deployment_config, fine_tuning_config),
            )
            evaluation_results = self.agent_designer.evaluate(agent_spec)
            quality_score = (
                self.agent_designer.score_quality(agent_spec)
                + self.rag_engine.score_quality(rag_config)
                + self.prompt_engineer.score_quality(prompt_templates)
                + self.llmops_manager.score_quality(deployment_config, monitoring_config)
            ) / 4.0

        explanation = self._generate_explanation(op, quality_score, recommendations)
        return AIEngineerReport(
            request_id=request.request_id,
            operation=op.value,
            agent_spec=agent_spec,
            rag_config=rag_config,
            prompt_templates=prompt_templates,
            fine_tuning_config=fine_tuning_config,
            deployment_config=deployment_config,
            monitoring_config=monitoring_config,
            evaluation_results=evaluation_results,
            cost_estimate=cost_estimate,
            recommendations=recommendations,
            quality_score=quality_score,
            explanation=explanation,
        )

    def _aggregate_costs(self, *cost_dicts: dict[str, float]) -> dict[str, float]:
        aggregated: dict[str, float] = {}
        for d in cost_dicts:
            for key, value in d.items():
                aggregated[key] = aggregated.get(key, 0.0) + value
        return aggregated

    def _generate_explanation(self, operation: Any, quality_score: float, recommendations: list[str]) -> str:
        op_name = operation.value if hasattr(operation, "value") else str(operation)
        recs_summary = f"{len(recommendations)} rekomendasi" if recommendations else "tidak ada rekomendasi"
        return (
            f"Desain AI untuk operasi '{op_name}' telah dihasilkan dengan skor kualitas "
            f"{quality_score:.0%}. {recs_summary} disertakan untuk peningkatan."
        )


ai_engineer_engine = AIEngineerEngine()
