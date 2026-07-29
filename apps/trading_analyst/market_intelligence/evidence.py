"""
Evidence Builder
================

Aggregates raw evidence from MarketAnalyzer into structured evidence.
Assigns initial confidence per evidence based on strength, consistency,
and cross-timeframe confirmation.

Does NOT produce decisions — only structured evidence.
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import Evidence, Bias

logger = logging.getLogger(__name__)

# Weight configuration for confidence scoring
CATEGORY_WEIGHTS = {
    "market_structure": 0.35,
    "trend": 0.25,
    "volume": 0.20,
    "volatility": 0.10,
    "session": 0.10,
}


class EvidenceBuilder:
    """
    Builds and refines evidence from raw analysis output.

    Stages:
    1. Aggregate evidence from analyzer categories
    2. Cross-timeframe confirmation
    3. Confidence adjustment based on consistency
    4. Final evidence list with calibrated confidence
    """

    def __init__(self):
        self._all_evidence: list[Evidence] = []
        self._timeframes_analyzed: list[str] = []

    def build(self, raw: dict[str, list[Evidence]], timeframes: list[str]) -> list[Evidence]:
        """
        Build structured evidence from raw analyzer output.

        Args:
            raw: Dict mapping category -> list[Evidence] from MarketAnalyzer
            timeframes: List of timeframes that were analyzed

        Returns:
            List of refined Evidence objects with calibrated confidence
        """
        self._timeframes_analyzed = timeframes
        self._all_evidence = []

        # Flatten all evidence
        for category, ev_list in raw.items():
            for ev in ev_list:
                # Ensure type is set correctly
                if not ev.type:
                    ev.type = category
                self._all_evidence.append(ev)

        # Cross-timeframe confirmation
        self._apply_cross_timeframe_boost()
        self._deduplicate()
        self._normalize_confidence()

        return sorted(self._all_evidence, key=lambda e: e.confidence, reverse=True)

    def _apply_cross_timeframe_boost(self) -> None:
        """
        Boost confidence for evidence confirmed across multiple timeframes.

        If the same evidence direction appears on multiple timeframes,
        its confidence gets a boost proportional to the number of confirmations.
        """
        if len(self._timeframes_analyzed) < 2:
            return

        # Group evidence by type + direction
        groups: dict[str, list[Evidence]] = {}
        for ev in self._all_evidence:
            key = f"{ev.type}:{ev.direction}"
            if key not in groups:
                groups[key] = []
            groups[key].append(ev)

        # For groups with evidence on multiple timeframes, boost confidence
        for key, ev_list in groups.items():
            unique_timeframes = set(e.timeframe for e in ev_list)
            confirmation_count = len(unique_timeframes)
            if confirmation_count >= 2:
                boost = min(0.1 * (confirmation_count - 1), 0.3)
                for ev in ev_list:
                    ev.confidence = min(1.0, ev.confidence + boost)
                    ev.strength = min(1.0, ev.strength + boost * 0.5)

    def _deduplicate(self) -> None:
        """
        Remove duplicate evidence items.

        If two evidence items have the same type + description + timeframe,
        keep the one with higher confidence.
        """
        seen: dict[str, Evidence] = {}
        deduped: list[Evidence] = []

        for ev in self._all_evidence:
            key = f"{ev.type}:{ev.description}:{ev.timeframe}"
            if key in seen:
                if ev.confidence > seen[key].confidence:
                    deduped.remove(seen[key])
                    deduped.append(ev)
                    seen[key] = ev
                # else keep the existing one
            else:
                deduped.append(ev)
                seen[key] = ev

        self._all_evidence = deduped

    def _normalize_confidence(self) -> None:
        """Normalize confidence values so the highest confidence item is 1.0."""
        if not self._all_evidence:
            return

        max_conf = max(e.confidence for e in self._all_evidence)
        if max_conf > 0:
            for ev in self._all_evidence:
                ev.confidence = min(1.0, ev.confidence / max_conf)

    def compute_weighted_bias(self) -> tuple[Bias, float]:
        """
        Compute overall market bias using weighted confidence scoring.

        Weights:
          - Market Structure: 35%
          - Trend: 25%
          - Volume: 20%
          - Volatility: 10%
          - Session: 10%

        Returns:
            (Bias, confidence_score) where confidence_score is 0.0 - 1.0
        """
        if not self._all_evidence:
            return Bias.NEUTRAL, 0.0

        # Group evidence by category
        by_category: dict[str, list[Evidence]] = {}
        for ev in self._all_evidence:
            cat = ev.type
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(ev)

        total_score = 0.0
        total_weight = 0.0

        for category, weight in CATEGORY_WEIGHTS.items():
            ev_list = by_category.get(category, [])
            if not ev_list:
                continue

            # Compute category score: bullish evidence sum - bearish evidence sum
            cat_score = 0.0
            for ev in ev_list:
                if ev.direction == "bullish":
                    cat_score += ev.strength * ev.confidence
                elif ev.direction == "bearish":
                    cat_score -= ev.strength * ev.confidence
                # neutral contributes 0

            # Normalize by number of evidence items
            if ev_list:
                cat_score = cat_score / len(ev_list)

            total_score += cat_score * weight
            total_weight += weight

        if total_weight == 0:
            return Bias.NEUTRAL, 0.0

        normalized_score = total_score / total_weight

        # Determine bias
        if normalized_score > 0.15:
            bias = Bias.BULLISH
        elif normalized_score < -0.15:
            bias = Bias.BEARISH
        else:
            bias = Bias.NEUTRAL

        confidence = min(1.0, abs(normalized_score) * 2)

        return bias, confidence

    def get_top_evidence(self, n: int = 5) -> list[Evidence]:
        """Return top N evidence items by confidence."""
        sorted_ev = sorted(self._all_evidence, key=lambda e: e.confidence, reverse=True)
        return sorted_ev[:n]

    def get_evidence_by_category(self) -> dict[str, list[Evidence]]:
        """Group evidence by type/category."""
        by_cat: dict[str, list[Evidence]] = {}
        for ev in self._all_evidence:
            if ev.type not in by_cat:
                by_cat[ev.type] = []
            by_cat[ev.type].append(ev)
        return by_cat
