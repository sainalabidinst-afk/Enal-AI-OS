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

from typing import Any

from apps.base import BaseReferenceApp
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
from apps.decision_intelligence.simulation_engine import SimulationEngine, SimulationOutcome
from apps.decision_intelligence.debate_engine import DebateEngine, DebateResult, StrategyVote


class DecisionIntelligenceApp(BaseReferenceApp):
    name = "decision-intelligence"
    version = "1.0.0"
    description = "Evidence-based decision analysis and explainable reasoning"
    category = "decision-intelligence"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DecisionIntelligenceWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("context", user_input)
        return await self.worker.execute(task)


def get_app() -> DecisionIntelligenceApp:
    return DecisionIntelligenceApp()

__all__ = [
    "DecisionIntelligenceApp",
    "get_app",
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
