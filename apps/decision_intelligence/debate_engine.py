"""
Debate Engine — multi-strategy comparison for decision alternatives.

Compares alternatives across multiple reasoning strategies (e.g., risk-averse,
growth-first, cost-minimizing) and produces a structured comparison that
highlights trade-offs, conflicts, and consensus areas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apps.decision_intelligence.schemas import EvidenceSource, Objective, RiskProfile


@dataclass
class StrategyVote:
    """A single strategy's evaluation of an alternative."""

    strategy_name: str
    alternative_description: str
    score: float = 0.0
    rationale: str = ""
    concerns: list[str] = field(default_factory=list)


@dataclass
class DebateResult:
    """Structured outcome of the debate engine."""

    alternative_description: str
    strategy_votes: list[StrategyVote] = field(default_factory=list)
    consensus_score: float = 0.0
    conflict_areas: list[str] = field(default_factory=list)
    winning_strategies: list[str] = field(default_factory=list)


class DebateEngine:
    """
    Compares decision alternatives across multiple reasoning strategies.

    Usage::

        engine = DebateEngine()
        debate = engine.debate(alternative_descriptions, evidence_set, objectives)
    """

    def __init__(self) -> None:
        self.strategies = [
            self._risk_averse_strategy,
            self._growth_first_strategy,
            self._cost_minimizing_strategy,
            self._evidence_first_strategy,
        ]

    def debate(
        self,
        alternative_descriptions: list[str],
        evidence_set: Any,
        objectives: list[Objective],
        risk_profiles: list[RiskProfile] | None = None,
    ) -> list[DebateResult]:
        """
        Run multi-strategy debate across alternatives.

        Args:
            alternative_descriptions: List of alternative descriptions.
            evidence_set: Aggregated evidence.
            objectives: Weighted objectives.
            risk_profiles: Optional per-alternative risk profiles.

        Returns:
            List of DebateResult, one per alternative.
        """
        risk_profiles = risk_profiles or []
        results: list[DebateResult] = []
        for idx, desc in enumerate(alternative_descriptions):
            risk_profile = risk_profiles[idx] if idx < len(risk_profiles) else RiskProfile()
            votes: list[StrategyVote] = []
            for strategy_fn in self.strategies:
                vote = strategy_fn(desc, evidence_set, objectives, risk_profile)
                votes.append(vote)
            consensus = sum(v.score for v in votes) / len(votes) if votes else 0.0
            conflicts = self._detect_conflicts(votes)
            winners = [v.strategy_name for v in votes if v.score >= consensus]
            results.append(DebateResult(
                alternative_description=desc,
                strategy_votes=votes,
                consensus_score=round(consensus, 4),
                conflict_areas=conflicts,
                winning_strategies=winners,
            ))
        return results

    def _risk_averse_strategy(
        self,
        description: str,
        evidence_set: Any,
        objectives: list[Objective],
        risk_profile: RiskProfile,
    ) -> StrategyVote:
        score = 1.0 - risk_profile.overall_risk
        rationale = "Prioritizes stability and low risk."
        concerns = []
        if risk_profile.probability > 0.5:
            concerns.append("High probability of adverse outcome")
        if risk_profile.impact > 0.7:
            concerns.append("High impact if failure occurs")
        return StrategyVote(
            strategy_name="risk_averse",
            alternative_description=description,
            score=round(score, 4),
            rationale=rationale,
            concerns=concerns,
        )

    def _growth_first_strategy(
        self,
        description: str,
        evidence_set: Any,
        objectives: list[Objective],
        risk_profile: RiskProfile,
    ) -> StrategyVote:
        base = 0.6
        for obj in objectives:
            if obj.goal == "maximize":
                base += obj.weight * 0.3
        score = min(1.0, base)
        rationale = "Prioritizes growth and maximizing objectives."
        concerns = ["May overlook downside risks"] if risk_profile.overall_risk > 0.3 else []
        return StrategyVote(
            strategy_name="growth_first",
            alternative_description=description,
            score=round(score, 4),
            rationale=rationale,
            concerns=concerns,
        )

    def _cost_minimizing_strategy(
        self,
        description: str,
        evidence_set: Any,
        objectives: list[Objective],
        risk_profile: RiskProfile,
    ) -> StrategyVote:
        cost_weight = 0.0
        for obj in objectives:
            if obj.name.lower() == "cost" and obj.goal == "minimize":
                cost_weight = obj.weight
                break
        score = 0.5 + cost_weight * 0.4
        rationale = "Prioritizes cost reduction."
        concerns = ["Cost cutting may reduce quality"] if score > 0.7 else []
        return StrategyVote(
            strategy_name="cost_minimizing",
            alternative_description=description,
            score=round(score, 4),
            rationale=rationale,
            concerns=concerns,
        )

    def _evidence_first_strategy(
        self,
        description: str,
        evidence_set: Any,
        objectives: list[Objective],
        risk_profile: RiskProfile,
    ) -> StrategyVote:
        if evidence_set is None or not getattr(evidence_set, "items", []):
            return StrategyVote(
                strategy_name="evidence_first",
                alternative_description=description,
                score=0.3,
                rationale="Insufficient evidence to support this alternative.",
                concerns=["Limited evidence base"],
            )
        avg_quality = getattr(evidence_set, "avg_quality", 0.5)
        sentiment = getattr(evidence_set, "dominant_sentiment", "neutral")
        base = avg_quality
        if sentiment == "positive":
            base += 0.15
        elif sentiment == "negative":
            base -= 0.1
        score = max(0.0, min(1.0, base))
        rationale = "Grounded in evidence quality and sentiment."
        concerns = ["Evidence may not cover all scenarios"] if score < 0.6 else []
        return StrategyVote(
            strategy_name="evidence_first",
            alternative_description=description,
            score=round(score, 4),
            rationale=rationale,
            concerns=concerns,
        )

    def _detect_conflicts(self, votes: list[StrategyVote]) -> list[str]:
        if not votes:
            return []
        scores = [v.score for v in votes]
        if max(scores) - min(scores) > 0.4:
            return ["Large disagreement across strategies"]
        return []
