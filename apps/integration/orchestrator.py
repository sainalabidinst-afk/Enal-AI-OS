"""
Integration Orchestrator
========================

Coordinates cross-capability workflows using:
- CapabilityRegistry for metadata-driven capability discovery
- CapabilityContext for shared mutable state
- WorkflowEngine for sequential step execution

This removes hardcoded capability coupling from the orchestrator.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.integration.context import CapabilityContext
from apps.integration.evidence_adapter import EvidenceAdapter, UnifiedEvidence
from apps.integration.registry import CapabilityDescriptor, capability_registry
from apps.integration.workflow import WorkflowEngine, WorkflowResult, WorkflowStep

logger = logging.getLogger(__name__)


class IntegrationEngine:
    """
    Builds and runs cross-capability workflows.

    Workflows are defined as sequences of steps that share a CapabilityContext.
    Capability relationships are declared in the CapabilityRegistry, not
    hardcoded in orchestrator methods.
    """

    def __init__(self) -> None:
        self._evidence_adapter = EvidenceAdapter()
        self._workflow_engine = WorkflowEngine()
        self._knowledge_store = None
        self._reasoning_engine = None
        self._trading_analyzer = None
        self._trading_summary_generator = None
        self._network_design_engine = None
        self._init_dependencies()
        self._register_workflows()

    def _init_dependencies(self) -> None:
        """Lazy-load dependencies to avoid circular imports."""
        try:
            from backend.app.core.knowledge.store import KnowledgeStore
            self._knowledge_store = KnowledgeStore()
        except Exception as e:
            logger.warning("KnowledgeStore not available: %s", e)

        try:
            from apps.organization.reasoning_engine import reasoning_engine
            self._reasoning_engine = reasoning_engine
        except Exception as e:
            logger.warning("ReasoningEngine not available: %s", e)

        try:
            from apps.trading_analyst.market_intelligence.analyzer import MarketAnalyzer
            from apps.trading_analyst.market_intelligence.summary import MarketSummaryGenerator
            self._trading_analyzer = MarketAnalyzer()
            self._trading_summary_generator = MarketSummaryGenerator()
        except Exception as e:
            logger.warning("Trading modules not available: %s", e)

        try:
            from apps.network_engineer.design_review import DesignReviewEngine
            self._network_design_engine = DesignReviewEngine()
        except Exception as e:
            logger.warning("Network DesignReviewEngine not available: %s", e)

    def _register_workflows(self) -> None:
        self._workflow_engine.register_step(
            WorkflowStep(
                name="trading_analysis",
                description="Fetch market data and produce structured evidence",
                func=self._step_trading_analysis,
            )
        )
        self._workflow_engine.register_step(
            WorkflowStep(
                name="knowledge_query",
                description="Query knowledge base for relevant entities and evidence",
                func=self._step_knowledge_query,
            )
        )
        self._workflow_engine.register_step(
            WorkflowStep(
                name="evidence_aggregation",
                description="Normalize and aggregate cross-capability evidence",
                func=self._step_evidence_aggregation,
            )
        )
        self._workflow_engine.register_step(
            WorkflowStep(
                name="reasoning",
                description="Run reasoning engine over facts and evidence",
                func=self._step_reasoning,
            )
        )
        self._workflow_engine.register_step(
            WorkflowStep(
                name="knowledge_persist",
                description="Persist aggregated result back to knowledge store",
                func=self._step_knowledge_persist,
            )
        )
        self._workflow_engine.register_step(
            WorkflowStep(
                name="network_design_review",
                description="Review network design against best practices",
                func=self._step_network_design_review,
            )
        )

    async def trading_analysis_with_knowledge(
        self,
        symbol: str,
        timeframes: list[str] | None = None,
        exchange: str = "binance",
    ) -> WorkflowResult:
        descriptor = capability_registry.resolve("trading-analysis")
        context = CapabilityContext(
            workflow_type="trading_analysis_with_knowledge",
            metadata={"capability_descriptor": descriptor.to_dict() if descriptor else {}},
        )
        context.set_input("symbol", symbol)
        context.set_input("timeframes", timeframes)
        context.set_input("exchange", exchange)

        result = await self._workflow_engine.run(
            "trading_analysis_with_knowledge",
            [
                WorkflowStep(name="trading_analysis", func=self._step_trading_analysis),
                WorkflowStep(name="knowledge_query", func=self._step_knowledge_query),
                WorkflowStep(name="evidence_aggregation", func=self._step_evidence_aggregation),
                WorkflowStep(name="reasoning", func=self._step_reasoning),
                WorkflowStep(name="knowledge_persist", func=self._step_knowledge_persist),
            ],
            context,
        )

        return self._to_integration_result(result, "trading_analysis_with_knowledge")

    async def network_design_review_with_knowledge(
        self,
        topology_description: str,
        requirements: str | None = None,
    ) -> WorkflowResult:
        descriptor = capability_registry.resolve("network-design-review")
        context = CapabilityContext(
            workflow_type="network_design_review_with_knowledge",
            metadata={"capability_descriptor": descriptor.to_dict() if descriptor else {}},
        )
        context.set_input("topology_description", topology_description)
        context.set_input("requirements", requirements)

        result = await self._workflow_engine.run(
            "network_design_review_with_knowledge",
            [
                WorkflowStep(name="network_design_review", func=self._step_network_design_review),
                WorkflowStep(name="knowledge_query", func=self._step_knowledge_query),
                WorkflowStep(name="reasoning", func=self._step_reasoning),
            ],
            context,
        )

        return self._to_integration_result(result, "network_design_review_with_knowledge")

    async def self_improvement_cycle(
        self,
        project_path: str,
        analysis_type: str = "full",
    ) -> WorkflowResult:
        descriptor = capability_registry.resolve("self-improvement")
        context = CapabilityContext(
            workflow_type="self_improvement_cycle",
            metadata={"capability_descriptor": descriptor.to_dict() if descriptor else {}},
        )
        context.set_input("project_path", project_path)
        context.set_input("analysis_type", analysis_type)

        result = await self._workflow_engine.run(
            "self_improvement_cycle",
            [
                WorkflowStep(name="self_improvement", func=self._step_self_improvement),
            ],
            context,
        )

        return self._to_integration_result(result, "self_improvement_cycle")

    async def _step_trading_analysis(self, context: CapabilityContext) -> CapabilityContext:
        if not self._trading_analyzer:
            context.set_intermediate("trading_error", "Trading analyzer not initialized")
            return context

        from apps.trading_analyst.market_intelligence.provider import build_trading_context, DEFAULT_TIMEFRAMES
        from apps.trading_analyst.market_intelligence.evidence import EvidenceBuilder

        symbol = context.get_input("symbol")
        timeframes = context.get_input("timeframes") or DEFAULT_TIMEFRAMES
        exchange = context.get_input("exchange", "binance")

        ctx = await build_trading_context(symbol, timeframes, exchange)
        raw_evidence = await self._trading_analyzer.analyze(ctx)

        evidence_builder = EvidenceBuilder()
        built_evidences = evidence_builder.build(raw_evidence, self._trading_analyzer.get_analyzed_timeframes())

        trading_evidences = [self._evidence_adapter.from_trading_evidence(ev) for ev in built_evidences]
        context.add_evidences(trading_evidences)
        context.set_intermediate("trading_evidence_count", len(trading_evidences))
        context.set_intermediate("analyzed_timeframes", self._trading_analyzer.get_analyzed_timeframes())
        context.set_metadata("step.trading_analysis.status", "completed")
        return context

    async def _step_knowledge_query(self, context: CapabilityContext) -> CapabilityContext:
        if not self._knowledge_store:
            context.set_intermediate("knowledge_error", "KnowledgeStore not available")
            return context

        from backend.app.core.knowledge.schema import KnowledgeDomain

        knowledge_evidences: list[UnifiedEvidence] = []
        knowledge_context: dict[str, Any] = {}

        symbol = context.get_input("symbol")
        topology_description = context.get_input("topology_description")
        query_text = symbol or topology_description or ""

        if query_text and symbol:
            trading_entities = self._knowledge_store.find_by_domain(KnowledgeDomain.TRADING)
            for entity in trading_entities[:10]:
                if entity.name.lower() in query_text.lower() or any(
                    tag.lower() in query_text.lower() for tag in entity.tags
                ):
                    knowledge_context[entity.id] = {
                        "name": entity.name,
                        "description": entity.description,
                        "confidence": entity.confidence,
                    }

            for entity in trading_entities[:5]:
                for claim_id in entity.evidence[:3]:
                    for k_ev in self._knowledge_store.get_evidence(claim_id):
                        knowledge_evidences.append(self._evidence_adapter.from_knowledge_evidence(k_ev))

        if topology_description and not symbol:
            network_entities = self._knowledge_store.find_by_domain(KnowledgeDomain.NETWORK)
            for entity in network_entities[:10]:
                knowledge_context[entity.id] = {
                    "name": entity.name,
                    "description": entity.description,
                    "confidence": entity.confidence,
                    "type": entity.type.value,
                }

        context.add_evidences(knowledge_evidences)
        context.set_intermediate("knowledge_evidence_count", len(knowledge_evidences))
        context.set_intermediate("knowledge_context", knowledge_context)
        context.set_metadata("step.knowledge_query.status", "completed")
        return context

    async def _step_evidence_aggregation(self, context: CapabilityContext) -> CapabilityContext:
        all_evidences = list(context.evidences)
        if all_evidences:
            aggregated = self._evidence_adapter.aggregate(all_evidences)
            context.add_evidence(aggregated)
            context.set_intermediate("aggregated_confidence", aggregated.confidence)
        else:
            context.set_intermediate("aggregated_confidence", 0.0)
        context.set_metadata("step.evidence_aggregation.status", "completed")
        return context

    async def _step_reasoning(self, context: CapabilityContext) -> CapabilityContext:
        reasoning_output: dict[str, Any] = {}
        if self._reasoning_engine and hasattr(self._reasoning_engine, "forward_chaining"):
            try:
                facts = [e.to_dict() for e in context.evidences[:20]]
                goal = (
                    f"Analyze market condition for {context.get_input('symbol')}"
                    if context.get_input("symbol")
                    else "Evaluate design against best practices"
                )
                reasoning_result = self._reasoning_engine.forward_chaining(
                    facts=facts,
                    goal=goal,
                )
                reasoning_output = {
                    "conclusions": getattr(reasoning_result, "conclusions", []),
                    "confidence": getattr(reasoning_result, "confidence", 0.0),
                }
            except Exception as e:
                logger.warning("Reasoning engine failed: %s", e)
                reasoning_output = {"error": str(e)}
        context.set_intermediate("reasoning_output", reasoning_output)
        context.set_metadata("step.reasoning.status", "completed")
        return context

    async def _step_knowledge_persist(self, context: CapabilityContext) -> CapabilityContext:
        if not self._knowledge_store:
            return context

        aggregated = next((e for e in context.evidences if e.id.startswith("aggregated_")), None)
        if not aggregated:
            return context

        try:
            from backend.app.core.knowledge.schema import (
                KnowledgeEntity,
                KnowledgeDomain,
                KnowledgeCategory,
                KnowledgeType,
                KnowledgeStatus,
            )
            import uuid as uuid_module

            symbol = context.get_input("symbol")
            exchange = context.get_input("exchange", "binance")
            timeframes = context.get_input("timeframes") or ["15m", "1h", "4h", "1d"]

            entity = KnowledgeEntity(
                id=f"trading_analysis_{uuid_module.uuid4().hex[:8]}",
                domain=KnowledgeDomain.TRADING,
                category=KnowledgeCategory.EVIDENCE,
                type=KnowledgeType.EVIDENCE,
                name=f"Market Analysis: {symbol}" if symbol else "Integrated Analysis",
                description=(
                    f"Integrated trading analysis for {symbol} on {exchange}"
                    if symbol
                    else "Integrated analysis result"
                ),
                status=KnowledgeStatus.VALIDATED,
                confidence=aggregated.confidence,
                evidence=[e.id for e in context.evidences[:10]],
                metadata={
                    "symbol": symbol,
                    "exchange": exchange,
                    "timeframes": timeframes,
                    "workflow_id": context.workflow_id,
                },
            )
            self._knowledge_store.register(entity)
            context.set_intermediate("persisted_entity_id", entity.id)
        except Exception as e:
            logger.warning("Failed to persist to knowledge store: %s", e)

        context.set_metadata("step.knowledge_persist.status", "completed")
        return context

    async def _step_network_design_review(self, context: CapabilityContext) -> CapabilityContext:
        design_review: dict[str, Any] = {}
        if self._network_design_engine:
            try:
                design_review = {
                    "status": "simulated",
                    "topology_description": context.get_input("topology_description"),
                    "requirements": context.get_input("requirements"),
                    "findings": [],
                }
            except Exception as e:
                logger.warning("Design review failed: %s", e)
                design_review = {"status": "error", "error": str(e)}
        context.set_intermediate("design_review", design_review)
        context.set_metadata("step.network_design_review.status", "completed")
        return context

    async def _step_self_improvement(self, context: CapabilityContext) -> CapabilityContext:
        context.set_intermediate(
            "self_improvement",
            {
                "project_path": context.get_input("project_path"),
                "analysis_type": context.get_input("analysis_type", "full"),
                "status": "roadmap",
                "message": "Self-improvement S1 not yet implemented",
            },
        )
        context.set_metadata("step.self_improvement.status", "completed")
        return context

    def _to_integration_result(self, workflow_result: WorkflowResult, workflow_type: str) -> WorkflowResult:
        return workflow_result


integration_engine = IntegrationEngine()
