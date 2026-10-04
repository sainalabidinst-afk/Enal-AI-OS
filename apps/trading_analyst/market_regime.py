"""
Market Regime Detection for Trading Analyst.

Identifies market regimes: bull, bear, sideways, high-volatility.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MarketRegime:
    """Detected market regime."""

    regime: str = "sideways"
    confidence: float = 0.0
    volatility: str = "normal"
    trend_strength: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class MarketRegimeDetector:
    """Detect market regime from price data."""

    def detect(self, closes: list[float], volumes: list[float], lookback: int = 20) -> MarketRegime:
        """Detect market regime."""
        if len(closes) < lookback:
            return MarketRegime()
        recent_closes = closes[-lookback:]
        sma = sum(recent_closes) / len(recent_closes)
        current_price = closes[-1]
        above_sma = sum(1 for p in recent_closes if p > sma)
        trend_ratio = above_sma / len(recent_closes)
        price_change = (
            (current_price - recent_closes[0]) / recent_closes[0] if recent_closes[0] > 0 else 0.0
        )
        volatility = "normal"
        if len(recent_closes) >= 10:
            returns = [
                (recent_closes[i] - recent_closes[i - 1]) / recent_closes[i - 1]
                for i in range(1, len(recent_closes))
                if recent_closes[i - 1] > 0
            ]
            if returns:
                avg_return = sum(returns) / len(returns)
                variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
                std_dev = variance**0.5
                if std_dev > 0.03:
                    volatility = "high"
                elif std_dev < 0.005:
                    volatility = "low"
        if trend_ratio > 0.7 and price_change > 0.02:
            regime = "bull"
            confidence = 0.8
        elif trend_ratio < 0.3 and price_change < -0.02:
            regime = "bear"
            confidence = 0.8
        elif volatility == "high":
            regime = "high_volatility"
            confidence = 0.7
        else:
            regime = "sideways"
            confidence = 0.6
        return MarketRegime(
            regime=regime,
            confidence=confidence,
            volatility=volatility,
            trend_strength=abs(trend_ratio - 0.5) * 2,
            metadata={
                "trend_ratio": trend_ratio,
                "price_change": price_change,
                "lookback": lookback,
            },
        )
