"""
Confidence Estimator
=====================

Estimates confidence with uncertainty quantification.
"""

import logging
from typing import Any

from apps.research_assistant.schemas import (
    ConfidenceLevel,
    Contradiction,
    Evidence,
    SourceQuality,
)

logger = logging.getLogger(__name__)


class ConfidenceEstimator:
    """Estimates confidence with uncertainty quantification."""

    def estimate(self, evidence_list: list[Evidence], contradictions: list[Contradiction]) -> tuple[float, ConfidenceLevel, list[str]]:
        if not evidence_list:
            return 0.0, ConfidenceLevel.very_low, ["No evidence available"]

        evidence_conf = [ev.confidence for ev in evidence_list]
        avg_evidence_conf = sum(evidence_conf) / len(evidence_conf)

        source_quality_scores = {
            SourceQuality.peer_reviewed: 0.9,
            SourceQuality.expert_review: 0.75,
            SourceQuality.editorial: 0.6,
            SourceQuality.unverified: 0.4,
        }
        quality_scores = [source_quality_scores.get(ev.source_quality, 0.5) for ev in evidence_list]
        avg_quality = sum(quality_scores) / len(quality_scores)

        contradiction_penalty = min(0.3, len(contradictions) * 0.05)

        confidence = (avg_evidence_conf * 0.5) + (avg_quality * 0.35) + (0.15 * (1.0 - contradiction_penalty))
        confidence = max(0.0, min(1.0, confidence))

        if confidence >= 0.9:
            level = ConfidenceLevel.very_high
        elif confidence >= 0.75:
            level = ConfidenceLevel.high
        elif confidence >= 0.6:
            level = ConfidenceLevel.moderate
        elif confidence >= 0.4:
            level = ConfidenceLevel.low
        else:
            level = ConfidenceLevel.very_low

        uncertainty: list[str] = []
        if contradiction_penalty > 0:
            uncertainty.append(f"{len(contradictions)} contradictions detected")
        if avg_quality < 0.7:
            uncertainty.append("Source quality varies")
        if len(evidence_list) < 5:
            uncertainty.append("Limited evidence base")
        if any(ev.recency_score < 0.3 for ev in evidence_list):
            uncertainty.append("Some sources are outdated")

        return confidence, level, uncertainty
