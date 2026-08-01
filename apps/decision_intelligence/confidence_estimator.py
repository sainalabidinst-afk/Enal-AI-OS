"""
Confidence Estimation — quantify uncertainty.

Produces explicit confidence scores (0-1) with uncertainty bounds,
informed by evidence quality, evidence agreement, and decision clarity.
"""

from __future__ import annotations

from typing import Any

from apps.decision_intelligence.schemas import ConfidenceScore


class ConfidenceEstimator:
    """
    Estimates confidence for a decision.

    Confidence is derived from:
        - Evidence quality (avg quality score)
        - Evidence agreement (positive vs. negative weight spread)
        - Evidence coverage (proportion of sources with data)
        - Decision margin (score gap between best and second alternative)

    Usage::

        estimator = ConfidenceEstimator()
        conf = estimator.estimate(evidence_set, top_scores)
    """

    def estimate(
        self,
        evidence_set: Any,
        top_scores: list[float] | None = None,
        evidence_count: int = 0,
    ) -> ConfidenceScore:
        """
        Estimate confidence in the recommended decision.

        Args:
            evidence_set: Processed EvidenceSet.
            top_scores: Sorted list of alternative scores (best first).
            evidence_count: Number of evidence items used.

        Returns:
            ConfidenceScore with score, uncertainty bound, explanation.
        """
        if evidence_set is None:
            avg_quality = 0.5
            agreement = 0.0
        else:
            avg_quality = evidence_set.avg_quality
            # Agreement = how one-sided the evidence is (0 = split, 1 = unanimous).
            total = evidence_set.positive_weight + evidence_set.negative_weight + evidence_set.neutral_weight
            agreement = max(evidence_set.positive_weight, evidence_set.negative_weight) / total if total > 0 else 0.0

        # Evidence coverage.
        coverage = min(1.0, evidence_count / 5.0)  # 5+ evidence items = full coverage

        # Decision margin: spread between best and second best.
        margin = 0.5
        if top_scores and len(top_scores) >= 2:
            margin = min(1.0, max(0.0, top_scores[0] - top_scores[1]))

        # Weighted confidence.
        confidence = (
            0.35 * avg_quality
            + 0.25 * agreement
            + 0.20 * coverage
            + 0.20 * margin
        )
        confidence = max(0.0, min(1.0, round(confidence, 4)))

        # Uncertainty bound widens as evidence quality drops.
        uncertainty_bound = round(0.15 + (0.25 * (1 - avg_quality)), 4)
        uncertainty_bound = max(0.0, min(0.5, uncertainty_bound))

        # Explanation.
        reasons: list[str] = []
        reasons.append(f"Evidence quality: {avg_quality:.0%}")
        reasons.append(f"Evidence agreement: {agreement:.0%}")
        reasons.append(f"Evidence coverage: {coverage:.0%}")
        if top_scores and len(top_scores) >= 2:
            reasons.append(f"Decision margin: {margin:.0%}")
        explanation = "; ".join(reasons)

        if confidence < 0.5:
            explanation += ". Confidence is low — consider gathering more evidence or deferring."

        return ConfidenceScore(
            score=confidence,
            uncertainty_bound=uncertainty_bound,
            explanation=explanation,
        )
