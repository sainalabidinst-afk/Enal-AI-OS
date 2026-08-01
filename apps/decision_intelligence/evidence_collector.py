"""
Evidence Collection — collect, validate, and structure evidence.

Collects evidence from multiple sources (Capability Pack outputs, API
responses, benchmark data, real-case files), scores quality, and produces
a weighted synthesis that downstream stages consume.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apps.decision_intelligence.schemas import EvidenceSource, EvidenceSourceType


@dataclass
class WeightedEvidence:
    """A processed evidence item with computed effective weight."""

    source_id: str
    evidence_type: EvidenceSourceType
    payload: dict[str, Any]
    quality_score: float
    raw_weight: float
    effective_weight: float  # quality_score × raw_weight
    sentiment: str = "neutral"  # extracted directional support: positive/negative/neutral
    weight_normalized: float = 0.0


@dataclass
class EvidenceSet:
    """Aggregated evidence collection with summary statistics."""

    items: list[WeightedEvidence] = field(default_factory=list)
    total_effective_weight: float = 0.0
    positive_weight: float = 0.0
    negative_weight: float = 0.0
    neutral_weight: float = 0.0
    avg_quality: float = 0.0

    @property
    def count(self) -> int:
        return len(self.items)

    @property
    def dominant_sentiment(self) -> str:
        """Return the sentiment carrying the most effective weight."""
        if self.positive_weight >= self.negative_weight and self.positive_weight >= self.neutral_weight:
            if self.positive_weight > 0.0:
                return "positive"
        if self.negative_weight >= self.neutral_weight:
            if self.negative_weight > 0.0:
                return "negative"
        return "neutral"


class EvidenceCollector:
    """
    Collects and processes evidence from one or more sources.

    Usage::

        collector = EvidenceCollector()
        evidence_set = collector.collect(evidence_sources)
    """

    # Keys commonly used in payloads to infer directional sentiment.
    _SENTIMENT_KEYS = ("sentiment", "bias", "direction", "recommendation", "grade", "outcome")

    def collect(self, sources: list[EvidenceSource]) -> EvidenceSet:
        """
        Process a list of evidence sources into a weighted EvidenceSet.

        Args:
            sources: Raw evidence sources from the DecisionRequest.

        Returns:
            EvidenceSet with weighted, normalized evidence.
        """
        items: list[WeightedEvidence] = []
        for source in sources:
            item = self._process_source(source)
            items.append(item)

        # Normalize weights across all items so they sum to 1.
        total_raw = sum(i.effective_weight for i in items) or 1.0
        for item in items:
            item.weight_normalized = item.effective_weight / total_raw

        pos = sum(i.weight_normalized for i in items if i.sentiment == "positive")
        neg = sum(i.weight_normalized for i in items if i.sentiment == "negative")
        neu = sum(i.weight_normalized for i in items if i.sentiment == "neutral")
        avg_q = sum(i.quality_score for i in items) / len(items) if items else 0.0

        return EvidenceSet(
            items=items,
            total_effective_weight=sum(i.effective_weight for i in items),
            positive_weight=pos,
            negative_weight=neg,
            neutral_weight=neu,
            avg_quality=avg_q,
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _process_source(self, source: EvidenceSource) -> WeightedEvidence:
        """Convert a single source into weighted evidence with sentiment."""
        sentiment = self._extract_sentiment(source.payload)
        effective_weight = source.quality_score * source.weight
        return WeightedEvidence(
            source_id=source.source_id,
            evidence_type=source.evidence_type,
            payload=source.payload,
            quality_score=source.quality_score,
            raw_weight=source.weight,
            effective_weight=effective_weight,
            sentiment=sentiment,
        )

    def _extract_sentiment(self, payload: dict[str, Any]) -> str:
        """
        Infer positive/negative/neutral direction from a payload.

        Looks for sentiment-related keys; falls back to inspecting
        numeric values in common fields such as 'score', 'confidence',
        or 'risk'.
        """
        for key in self._SENTIMENT_KEYS:
            val = payload.get(key)
            if isinstance(val, str):
                lowered = val.lower()
                if lowered in ("bullish", "positive", "buy", "pass", "recommend", "yes", "up", "high"):
                    return "positive"
                if lowered in ("bearish", "negative", "sell", "fail", "reject", "no", "down", "low", "high risk"):
                    return "negative"
                if lowered in ("neutral", "hold", "wait", "unknown"):
                    return "neutral"
            elif isinstance(val, (int, float)):
                # High positive scores / low risk values infer direction.
                if key in ("confidence", "score", "grade"):
                    return "positive" if val >= 0.7 else ("negative" if val < 0.4 else "neutral")
                if key in ("risk", "risk_score"):
                    return "negative" if val >= 0.7 else ("positive" if val < 0.4 else "neutral")

        # Fallback: examine generic numeric payload fields.
        for key in ("score", "confidence", "risk", "sentiment"):
            val = payload.get(key)
            if isinstance(val, (int, float)):
                if key == "risk":
                    return "negative" if val >= 0.7 else ("positive" if val < 0.4 else "neutral")
                return "positive" if val >= 0.7 else ("negative" if val < 0.4 else "neutral")

        # If we cannot infer direction, treat as neutral.
        return "neutral"
