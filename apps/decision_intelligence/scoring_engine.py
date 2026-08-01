"""
Decision Scoring — score and rank alternatives.

Combines trade-off composite scores with risk adjustments and evidence
alignment to produce a final rank order of alternatives.
"""

from __future__ import annotations

from typing import Any

from apps.decision_intelligence.schemas import Objective, RiskTolerance, TradeOff


class ScoringEngine:
    """
    Scores and ranks decision alternatives.

    Usage::

        scorer = ScoringEngine()
        ranked = scorer.score_alternatives(alts, objectives, evidence_set, risk_tolerance)
    """

    def score_alternatives(
        self,
        alternatives: list[dict[str, Any]],
        objectives: list[Objective],
        evidence_set: Any = None,
        risk_tolerance: RiskTolerance = RiskTolerance.medium,
    ) -> list[dict[str, Any]]:
        """
        Score each alternative and sort by composite score descending.

        Score formula:
            composite = tradeoff_composite * (1 - risk_penalty_weight * risk_value)

        The risk penalty term is scaled by tolerance (low tolerance penalizes
        risk more).

        Args:
            alternatives: List of alternative dicts with keys:
                          description, risk_profile.
            objectives: Weighted objectives for trade-off scoring.
            evidence_set: Processed evidence set.
            risk_tolerance: Risk tolerance level.

        Returns:
            Alternatives sorted by score (best first), each with a
            'score' key added.
        """
        risk_penalty_weight = {
            RiskTolerance.low: 0.35,
            RiskTolerance.medium: 0.25,
            RiskTolerance.high: 0.15,
        }[risk_tolerance]

        scored: list[dict[str, Any]] = []
        for alt in alternatives:
            description = alt["description"]
            # Reuse tradeoff analyzer for composite score.
            tradeoff_composite = self._tradeoff_composite(description, objectives, evidence_set)

            risk_profile = alt.get("risk_profile")
            risk_value = risk_profile.overall_risk if risk_profile is not None else 0.5

            # Composite = tradeoff score scaled by risk penalty.
            # When risk tolerance is low, risk penalizes the score more.
            composite = tradeoff_composite * (1 - risk_penalty_weight * risk_value)
            composite = max(0.0, min(1.0, round(composite, 4)))
            alt_with_score = dict(alt)
            alt_with_score["score"] = composite
            alt_with_score["tradeoff_composite"] = tradeoff_composite
            scored.append(alt_with_score)

        scored.sort(key=lambda a: a["score"], reverse=True)
        return scored

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _tradeoff_composite(self, description: str, objectives: list[Objective], evidence_set: Any) -> float:
        """Compute composite trade-off score via TradeoffAnalyzer."""
        from apps.decision_intelligence.tradeoff_analyzer import TradeoffAnalyzer

        return TradeoffAnalyzer().compute_composite_score(description, objectives, evidence_set)


def rank_alternatives(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Return scored alternatives already sorted best-first.

    Kept as a convenience alias for callers that only need the ranking.
    """
    return scored
