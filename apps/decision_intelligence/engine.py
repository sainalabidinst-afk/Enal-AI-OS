"""
Decision Intelligence Engine — domain engine orchestrator.

Orchestrates the full decision pipeline:
    1. Evidence Collection
    2. Alternative Generation
    3. Risk Analysis
    4. Trade-off Analysis
    5. Decision Scoring
    6. Confidence Estimation
    7. Explanation Generation
    8. Decision History

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.decision_intelligence.schemas import (
    DecisionRequest,
    DecisionResult,
    DecisionOutcome,
    DecisionRecord,
    Alternative as AltSchema,
    RiskProfile,
    Explanation,
)
from apps.decision_intelligence.evidence_collector import EvidenceCollector, EvidenceSet
from apps.decision_intelligence.alternative_generator import AlternativeGenerator
from apps.decision_intelligence.risk_analyzer import RiskAnalyzer
from apps.decision_intelligence.tradeoff_analyzer import TradeoffAnalyzer
from apps.decision_intelligence.scoring_engine import ScoringEngine
from apps.decision_intelligence.confidence_estimator import ConfidenceEstimator
from apps.decision_intelligence.explanation_generator import ExplanationGenerator
from apps.decision_intelligence.decision_history import DecisionHistoryStore

logger = logging.getLogger(__name__)


class DecisionIntelligenceEngine:
    """
    Orchestrates the full decision intelligence pipeline.

    Public API::

        engine = DecisionIntelligenceEngine()
        result = engine.evaluate(request)
    """

    def __init__(self, history_store: DecisionHistoryStore | None = None) -> None:
        self.collector = EvidenceCollector()
        self.generator = AlternativeGenerator()
        self.risk = RiskAnalyzer()
        self.tradeoff = TradeoffAnalyzer()
        self.scorer = ScoringEngine()
        self.confidence = ConfidenceEstimator()
        self.explainer = ExplanationGenerator()
        self.history = history_store or DecisionHistoryStore()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(self, request: DecisionRequest) -> DecisionResult:
        """
        Run the full decision pipeline.

        Args:
            request: DecisionRequest with context, evidence, objectives.

        Returns:
            DecisionResult with recommendation, alternatives, explanation.
        """
        started = time.monotonic()

        # 1. Evidence Collection.
        evidence_set = self.collector.collect(request.evidence_sources)

        # 2. Alternative Generation.
        raw_alts = self.generator.generate(
            context=request.context,
            evidence_set=evidence_set,
            constraints=request.constraints,
            max_alternatives=request.max_alternatives,
        )

        # 3. Risk Analysis.
        alt_dicts: list[dict[str, Any]] = []
        for alt in raw_alts:
            risk_profile = self.risk.analyze(
                description=alt.description,
                risk_tolerance=request.risk_tolerance,
                evidence_set=evidence_set,
            )
            alt_dicts.append({
                "description": alt.description,
                "feasibility": alt.feasibility,
                "risk_profile": risk_profile,
            })

        # 4. Trade-off & Scoring.
        scored = self.scorer.score_alternatives(
            alternatives=alt_dicts,
            objectives=request.objectives,
            evidence_set=evidence_set,
            risk_tolerance=request.risk_tolerance,
        )

        # 5. Confidence Estimation.
        top_scores = [a.get("score", 0.0) for a in scored]
        conf = self.confidence.estimate(
            evidence_set=evidence_set,
            top_scores=top_scores,
            evidence_count=len(request.evidence_sources),
        )

        # 6. Explanation Generation.
        explanation = self.explainer.generate(
            decision_id=request.decision_id,
            context=request.context,
            evidence_set=evidence_set,
            scored_alternatives=scored,
            confidence=conf,
            constraints=request.constraints,
        )

        # 7. Build output.
        recommended = scored[0]["description"] if scored else "No feasible alternative"
        alternatives_schema = self._build_alternatives_schema(scored)

        result = DecisionResult(
            decision_id=request.decision_id,
            recommended_decision=recommended,
            alternatives=alternatives_schema,
            confidence_score=conf.score,
            confidence_explanation=conf.explanation,
            explanation=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "evidence_count": evidence_set.count if evidence_set else 0,
                "alternatives_count": len(scored),
                "evidence_quality": round(evidence_set.avg_quality, 4) if evidence_set else 0.0,
                "dominant_sentiment": evidence_set.dominant_sentiment if evidence_set else "neutral",
            },
        )

        # 8. Decision History.
        record = DecisionRecord(
            decision_id=request.decision_id,
            context=request.context,
            chosen_alternative=recommended,
            alternatives_count=len(scored),
            confidence_score=conf.score,
            evidence_count=len(request.evidence_sources),
            risk_score=scored[0]["risk_profile"].overall_risk if scored and scored[0].get("risk_profile") else 0.0,
            explanation=explanation.final_rationale,
        )
        ref = self.history.record(record)
        result.decision_history_ref = ref

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_alternatives_schema(self, scored: list[dict[str, Any]]) -> list[AltSchema]:
        """Convert scored dicts to Alternative schema objects."""
        alternatives: list[AltSchema] = []
        for alt in scored:
            rp = alt.get("risk_profile")
            risk_profile = rp if isinstance(rp, RiskProfile) else RiskProfile()
            t = self.tradeoff.score_alternative(
                description=alt["description"],
                objectives=[],
                evidence_set=None,
            )
            alternatives.append(
                AltSchema(
                    description=alt["description"],
                    score=alt.get("score", 0.0),
                    confidence=alt.get("score", 0.0),
                    risk_profile=risk_profile,
                    trade_offs=t,
                )
            )
        return alternatives
