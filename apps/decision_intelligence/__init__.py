"""
Decision Intelligence — shared reasoning layer for ECP.

Provides evidence-based, explainable, and auditable decision-making
across all Capability Packs. Acts as a cross-cutting cognitive service
without modifying Core.

Pipeline:
    DecisionRequest
        ↓
    EvidenceCollection (collect, validate, weight)
        ↓
    AlternativeGeneration (enumerate, filter)
        ↓
    RiskAnalysis (probability × impact)
        ↓
    TradeoffAnalysis (multi-objective, weighted)
        ↓
    DecisionScoring (composite score, rank)
        ↓
    ConfidenceEstimation (0-100%, calibration)
        ↓
    ExplanationGeneration (full chain)
        ↓
    DecisionHistory (Experience Memory)
        ↓
    DecisionResult
"""

from apps.decision_intelligence.engine import DecisionIntelligenceEngine
from apps.decision_intelligence.worker import DecisionIntelligenceWorker
from apps.decision_intelligence.schemas import (
    DecisionRequest,
    DecisionResult,
    EvidenceSource,
    EvidenceSourceType,
    Objective,
    ObjectiveGoal,
    RiskTolerance,
    Alternative,
    RiskProfile,
    TradeOff,
    ConfidenceScore,
    Explanation,
    DecisionRecord,
    DecisionOutcome,
)

__all__ = [
    "DecisionIntelligenceEngine",
    "DecisionIntelligenceWorker",
    "DecisionRequest",
    "DecisionResult",
    "EvidenceSource",
    "EvidenceSourceType",
    "Objective",
    "ObjectiveGoal",
    "RiskTolerance",
    "Alternative",
    "RiskProfile",
    "TradeOff",
    "ConfidenceScore",
    "Explanation",
    "DecisionRecord",
    "DecisionOutcome",
]
