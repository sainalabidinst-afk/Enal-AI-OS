"""
Market Analyzer
===============

Produces FACTS about market conditions from TradingContext.
Does NOT produce trading decisions (BUY/SELL).

Output: structured facts organized by category:
  - market_structure: higher highs/lows, support/resistance
  - trend: EMA alignment, slope direction
  - volume: volume trend, volume profile
  - volatility: ATR, Bollinger Bands width
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import (
    TradingContext, OHLCV, Evidence,
)
from apps.trading_analyst.market_intelligence import indicators as ind

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """
    Analyzes market data and produces structured facts.
    Each method returns factual observations. No method returns a trading decision.
    """

    def __init__(self):
        self._analyzed_timeframes: list[str] = []

    async def analyze(self, ctx: TradingContext) -> dict[str, list[Evidence]]:
        """
        Run full analysis across all timeframes.
        Returns dict mapping category -> list[Evidence]
        Categories: market_structure, trend, volume, volatility
        """
        categories: dict[str, list[Evidence]] = {
            "market_structure": [],
            "trend": [],
            "volume": [],
            "volatility": [],
        }

        for tf, ohlcv_list in ctx.timeframes.items():
            if not ohlcv_list or len(ohlcv_list) < 20:
                logger.debug("Skipping %s: insufficient data (%d candles)", tf, len(ohlcv_list or []))
                continue

            self._analyzed_timeframes.append(tf)
            closes = [c.close for c in ohlcv_list]
            highs = [c.high for c in ohlcv_list]
            lows = [c.low for c in ohlcv_list]
            volumes = [c.volume for c in ohlcv_list]
            current_price = closes[-1]

            categories["market_structure"].extend(
                self._analyze_structure(ohlcv_list, tf, current_price)
            )
            categories["trend"].extend(
                self._analyze_trend(closes, tf)
            )
            categories["volume"].extend(
                self._analyze_volume(volumes, closes, tf)
            )
            categories["volatility"].extend(
                self._analyze_volatility(closes, highs, lows, tf)
            )

        return categories

    def _create_evidence(self, etype: str, description: str, tf: str,
                         strength: float, direction: str, source: str) -> Evidence:
        """Helper to create an Evidence instance with a unique ID."""
        evidence_id = f"{etype}_{tf}_{len(description)}"
        return Evidence(
            id=evidence_id,
            type=etype,
            description=description,
            timeframe=tf,
            strength=max(0.0, min(1.0, strength)),
            direction=direction,
            source=source,
            confidence=max(0.0, min(1.0, strength * 0.9 + 0.1)),
        )

    def _analyze_structure(self, ohlcv: list[OHLCV], tf: str,
                           current_price: float) -> list[Evidence]:
        """Analyze market structure: swing points, HH/HL, support/resistance."""
        evidence: list[Evidence] = []
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        closes = [c.close for c in ohlcv]

        # 1. Higher High / Lower Low detection
        swings = ind.detect_swing_points(highs, lows, window=5)
        if len(swings["highs"]) >= 2:
            last_highs = [highs[i] for i in swings["highs"][-3:]]
            if len(last_highs) >= 2 and last_highs[-1] > last_highs[-2]:
                evidence.append(self._create_evidence(
                    "market_structure",
                    f"Higher High formed on {tf}",
                    tf, 0.75, "bullish", "analyzer.structure"
                ))
            elif len(last_highs) >= 2 and last_highs[-1] < last_highs[-2]:
                evidence.append(self._create_evidence(
                    "market_structure",
                    f"Lower High formed on {tf}",
                    tf, 0.70, "bearish", "analyzer.structure"
                ))

        if len(swings["lows"]) >= 2:
            last_lows = [lows[i] for i in swings["lows"][-3:]]
            if len(last_lows) >= 2 and last_lows[-1] > last_lows[-2]:
                evidence.append(self._create_evidence(
                    "market_structure",
                    f"Higher Low formed on {tf}",
                    tf, 0.70, "bullish", "analyzer.structure"
                ))
            elif len(last_lows) >= 2 and last_lows[-1] < last_lows[-2]:
                evidence.append(self._create_evidence(
                    "market_structure",
                    f"Lower Low formed on {tf}",
                    tf, 0.75, "bearish", "analyzer.structure"
                ))

        # 2. Price vs recent range
        recent_high = max(highs[-20:]) if len(highs) >= 20 else max(highs)
        recent_low = min(lows[-20:]) if len(lows) >= 20 else min(lows)
        range_pct = (current_price - recent_low) / (recent_high - recent_low) if recent_high != recent_low else 0.5
        if range_pct > 0.75:
            evidence.append(self._create_evidence(
                "market_structure",
                f"Price near top of {tf} range ({(range_pct * 100):.0f}%)",
                tf, min(range_pct, 0.9), "bullish", "analyzer.structure"
            ))
        elif range_pct < 0.25:
            evidence.append(self._create_evidence(
                "market_structure",
                f"Price near bottom of {tf} range ({(range_pct * 100):.0f}%)",
                tf, min(1 - range_pct, 0.9), "bearish", "analyzer.structure"
            ))

        # 3. Support / Resistance proximity (using EMA as dynamic S/R proxy)
        ema50 = ind.compute_ema(closes, 50)
        ema200 = ind.compute_ema(closes, 200)
        if ema50 and closes[-1]:
            current = closes[-1]
            if ema50:
                dist_to_ema50 = abs(current - ema50[-1]) / current if current > 0 else 1
                if dist_to_ema50 < 0.005:
                    evidence.append(self._create_evidence(
                        "market_structure",
                        f"Price at EMA 50 ({ema50[-1]:.2f}) on {tf}",
                        tf, 0.75, "neutral", "analyzer.structure"
                    ))
            if ema200:
                dist_to_ema200 = abs(current - ema200[-1]) / current if current > 0 else 1
                if dist_to_ema200 < 0.005:
                    evidence.append(self._create_evidence(
                        "market_structure",
                        f"Price at EMA 200 ({ema200[-1]:.2f}) on {tf}",
                        tf, 0.80, "neutral", "analyzer.structure"
                    ))

        return evidence

    def _analyze_trend(self, closes: list[float], tf: str) -> list[Evidence]:
        """Analyze trend: EMA alignment, regression slope, MACD."""
        evidence: list[Evidence] = []

        # 1. EMA Alignment (20 vs 50)
        ema20 = ind.compute_ema(closes, 20)
        ema50 = ind.compute_ema(closes, 50)
        if ema20 and ema50:
            if ema20[-1] > ema50[-1]:
                evidence.append(self._create_evidence(
                    "trend",
                    f"EMA 20 > EMA 50 on {tf} (bullish alignment)",
                    tf, 0.70, "bullish", "analyzer.trend"
                ))
            else:
                evidence.append(self._create_evidence(
                    "trend",
                    f"EMA 20 < EMA 50 on {tf} (bearish alignment)",
                    tf, 0.70, "bearish", "analyzer.trend"
                ))

        # 2. Regression slope
        slope_data = closes[-50:] if len(closes) >= 50 else closes
        slope, _ = ind.compute_linear_regression(slope_data)
        if slope > 0:
            evidence.append(self._create_evidence(
                "trend",
                f"Positive regression slope on {tf} ({(slope * 100):.4f}%)",
                tf, min(abs(slope) * 100, 0.9), "bullish", "analyzer.trend"
            ))
        elif slope < 0:
            evidence.append(self._create_evidence(
                "trend",

