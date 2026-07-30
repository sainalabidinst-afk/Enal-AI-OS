"""
Market Summary Generator
========================

Generates a human-readable summary of market analysis using the
existing Reasoning Engine (no new LLM engine).

The Reasoning Engine takes structured evidence and produces:
- Market summary text
- Counter scenario
- Suggested strategy
- Reasoning steps
"""

import logging
from typing import Any
from datetime import datetime, timezone

from apps.trading_analyst.market_intelligence.models import (
    AnalysisResult, AnalysisMetadata, MarketEvidence, Bias, RiskLevel,
)
from apps.trading_analyst.market_intelligence.evidence import EvidenceBuilder
from apps.trading_analyst.market_intelligence.confidence import (
    compute_weighted_score, compute_risk_level,
)

logger = logging.getLogger(__name__)


class MarketSummaryGenerator:
    """
    Generates a structured market analysis summary.

    Uses the EvidenceBuilder + ConfidenceScorer for evidence processing,
    then produces the final AnalysisResult.

    Does NOT produce trading signals or recommendations.
    """

    def __init__(self):
        self._evidence_builder = EvidenceBuilder()

    def generate(
        self,
        raw_evidence: dict[str, list[MarketEvidence]],
        timeframes: list[str],
        symbol: str,
        exchange: str = "binance",
        latency_ms: float = 0.0,
    ) -> AnalysisResult:
        """
        Generate a complete market analysis result.

        Args:
            raw_evidence: Dict from MarketAnalyzer.analyze()
            timeframes: List of analyzed timeframes
            symbol: Trading pair (e.g., "BTCUSDT")
            exchange: Exchange name
            latency_ms: API latency in milliseconds

        Returns:
            AnalysisResult with structured output (call .to_dict() for JSON)
        """
        # Step 1: Build structured evidence
        evidence = self._evidence_builder.build(raw_evidence, timeframes)

        # Step 2: Compute weighted confidence score
        bias, confidence, category_scores = compute_weighted_score(evidence)

        # Step 3: Compute risk level
        risk_level_str = compute_risk_level(bias, confidence, evidence)
        risk_level = RiskLevel(risk_level_str)

        # Step 4: Generate summary text
        summary = self._build_summary(symbol, bias, confidence, evidence, category_scores)
        counter_scenario = self._build_counter_scenario(bias, evidence)
        suggested_strategy = self._build_strategy_suggestion(bias, confidence, risk_level)
        reasoning_steps = self._build_reasoning_steps(evidence, bias, confidence, category_scores)

        # Step 5: Build metadata
        metadata = AnalysisMetadata(
            symbol=symbol,
            exchange=exchange,
            timeframes=timeframes,
            generated_at=datetime.now(timezone.utc).isoformat(),
            data_source="binance_public_api",
            analysis_version="1.0.0",
            latency_ms=latency_ms,
            raw_data_points=sum(len(raw_evidence.get(cat, [])) for cat in raw_evidence),
        )

        # Get top evidence for raw field
        top_evidence = self._evidence_builder.get_top_evidence(10)

        return AnalysisResult(
            symbol=symbol,
            bias=bias,
            confidence=confidence,
            evidence=evidence,
            risk_level=risk_level,
            counter_scenario=counter_scenario,
            suggested_strategy=suggested_strategy,
            summary=summary,
            reasoning_steps=reasoning_steps,
            metadata=metadata,
            raw={
                "category_scores": {k: round(v, 4) for k, v in category_scores.items()},
                "top_evidence": [
                    {
                        "id": e.id,
                        "description": e.description,
                        "strength": round(e.strength, 2),
                        "confidence": round(e.confidence, 2),
                    }
                    for e in top_evidence
                ],
                "timeframes_analyzed": timeframes,
            },
        )

    def _build_summary(
        self,
        symbol: str,
        bias: Bias,
        confidence: float,
        evidence: list[MarketEvidence],
        category_scores: dict[str, float],
    ) -> str:
        """Build a human-readable market summary."""
        bias_label = bias.value.upper()
        confidence_pct = round(confidence * 100)

        # Count evidence by direction
        bullish = sum(1 for e in evidence if e.direction == "bullish")
        bearish = sum(1 for e in evidence if e.direction == "bearish")
        neutral = sum(1 for e in evidence if e.direction == "neutral")

        # Determine strongest category
        if category_scores:
            strongest_cat = max(category_scores, key=lambda k: category_scores[k] if category_scores[k] is not None else 0.0)
            strongest_score = category_scores[strongest_cat]
        else:
            strongest_cat = "unknown"
            strongest_score = 0.0

        summary_parts = [
            f"Market analysis for {symbol}: {bias_label} bias with {confidence_pct}% confidence.",
            f"Evidence breakdown: {bullish} bullish, {bearish} bearish, {neutral} neutral signals.",
            f"Strongest category: {strongest_cat.replace('_', ' ').title()} "
            f"(score: {abs(strongest_score):.2f}).",
        ]

        # Add top evidence descriptions
        top = self._evidence_builder.get_top_evidence(3)
        if top:
            summary_parts.append("Key observations:")
            for ev in top:
                summary_parts.append(f"  - {ev.description} ({ev.timeframe}, strength: {ev.strength:.2f})")

        return " ".join(summary_parts)

    def _build_counter_scenario(self, bias: Bias, evidence: list[MarketEvidence]) -> str:
        """Build a counter-scenario that could invalidate the current bias."""
        if bias == Bias.NEUTRAL:
            return (
                "Market is neutral with mixed signals. "
                "A breakout above resistance or breakdown below support "
                "would establish direction."
            )

        # Find contradictory evidence
        opposite = "bearish" if bias == Bias.BULLISH else "bullish"
        contradicting = [e for e in evidence if e.direction == opposite]

        if contradicting:
            top_counters = contradicting[:2]
            counter_desc = "; ".join(e.description for e in top_counters)
            return (
                f"Counter scenario: {counter_desc}. "
                f"If these signals strengthen, the current {bias.value} bias may weaken."
            )

        return (
            f"Counter scenario: A shift in {bias.value} momentum could occur "
            f"if key support/resistance levels are broken with high volume."
        )

    def _build_strategy_suggestion(
        self, bias: Bias, confidence: float, risk_level: RiskLevel
    ) -> str:
        """Build a generic strategy suggestion (not a trading signal)."""
        if bias == Bias.NEUTRAL:
            return "Await clearer direction. Market is in consolidation."

        confidence_label = "high" if confidence > 0.7 else "moderate" if confidence > 0.4 else "low"
        bias_label = bias.value

        return (
            f"{confidence_label.capitalize()} confidence {bias_label} bias with "
            f"{risk_level.value} risk. Consider aligning with the {bias_label} trend "
            f"but be aware of the counter scenario."
        )

    def _build_reasoning_steps(
        self,
        evidence: list[MarketEvidence],
        bias: Bias,
        confidence: float,
        category_scores: dict[str, float],
    ) -> list[str]:
        """Build reasoning trace for transparency."""
        steps = [
            f"1. Analyzed {len(evidence)} evidence items across {len(category_scores)} categories.",
            f"2. Weighted scoring applied: Market Structure 35%, Trend 25%, Volume 20%, Volatility 10%, Session 10%.",
            f"3. Overall bias: {bias.value.upper()} (confidence: {round(confidence * 100)}%).",
        ]

        for category, score in sorted(category_scores.items(), key=lambda x: abs(x[1]), reverse=True):
            direction = "bullish" if score > 0 else "bearish" if score < 0 else "neutral"
            steps.append(
                f"   - {category.replace('_', ' ').title()}: {direction} ({abs(score):.2f})"
            )

        # Top evidence
        top = self._evidence_builder.get_top_evidence(3)
        for ev in top:
            steps.append(f"4. Key factor: {ev.description} (confidence: {ev.confidence:.2f})")

        return steps
