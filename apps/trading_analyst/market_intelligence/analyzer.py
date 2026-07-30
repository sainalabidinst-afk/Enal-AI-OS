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
    TradingContext, OHLCV, MarketEvidence,
)
from apps.trading_analyst.market_intelligence import indicators as ind

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """
    Analyzes market data and produces structured facts.
    
    Each method produces factual observations only.
    No method returns a trading decision (BUY/SELL).
    """

    def __init__(self):
        self._analyzed_timeframes: list[str] = []

    async def analyze(self, ctx: TradingContext) -> dict[str, list[MarketEvidence]]:
        """
        Run full analysis across all timeframes.
        
        Returns dict mapping category -> list[MarketEvidence]
        Categories: market_structure, trend, volume, volatility
        """
        categories: dict[str, list[MarketEvidence]] = {
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

            # 1. Market Structure
            categories["market_structure"].extend(
                self._analyze_structure(ohlcv_list, tf, current_price)
            )

            # 2. Trend
            categories["trend"].extend(
                self._analyze_trend(closes, tf)
            )

            # 3. Volume
            categories["volume"].extend(
                self._analyze_volume(volumes, closes, tf)
            )

            # 4. Volatility
            categories["volatility"].extend(
                self._analyze_volatility(closes, highs, lows, tf)
            )

        return categories

    def _create_evidence(self, etype: str, description: str, tf: str,
                         strength: float, direction: str, source: str) -> MarketEvidence:
        """Helper to create an MarketEvidence instance with a unique ID."""
        evidence_id = f"{etype}_{tf}_{len(description)}"
        return MarketEvidence(
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
                           current_price: float) -> list[MarketEvidence]:
        """Analyze market structure: swing points, HH/HL, support/resistance."""
        evidence: list[MarketEvidence] = []
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        closes = [c.close for c in ohlcv]

        # 1. Higher High / Lower Low via swing points
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

        # 2. Price position in recent range
        if len(highs) >= 20:
            recent_high = max(highs[-20:])
            recent_low = min(lows[-20:])
        else:
            recent_high = max(highs)
            recent_low = min(lows)
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

        # 3. Support / Resistance proximity via swing points
        if swings["highs"] and swings["lows"]:
            nearest_support = max(lows[i] for i in swings["lows"][-3:]) if swings["lows"] else None
            nearest_resistance = min(highs[i] for i in swings["highs"][-3:]) if swings["highs"] else None
            if nearest_support is not None and current_price > 0:
                dist_to_support = abs(current_price - nearest_support) / current_price
                if dist_to_support < 0.01:
                    evidence.append(self._create_evidence(
                        "market_structure",
                        f"Price at support level ({nearest_support:.2f}) on {tf}",
                        tf, 0.80, "bullish", "analyzer.structure"
                    ))
            if nearest_resistance is not None and current_price > 0:
                dist_to_resistance = abs(current_price - nearest_resistance) / current_price
                if dist_to_resistance < 0.01:
                    evidence.append(self._create_evidence(
                        "market_structure",
                        f"Price at resistance level ({nearest_resistance:.2f}) on {tf}",
                        tf, 0.80, "bearish", "analyzer.structure"
                    ))

        return evidence

    def _analyze_trend(self, closes: list[float], tf: str) -> list[MarketEvidence]:
        """Analyze trend: EMA alignment, regression slope, MACD."""
        evidence: list[MarketEvidence] = []

        # 1. EMA Alignment
        ema20 = ind.compute_ema(closes, 20)
        ema50 = ind.compute_ema(closes, 50)
        if ema20 and ema50:
            last_ema20 = ema20[-1]
            last_ema50 = ema50[-1]
            if last_ema20 > last_ema50:
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
        slope, _ = ind.compute_linear_regression(closes[-50:]) if len(closes) >= 50 else (0, 0)
        if slope > 0:
            strength = min(abs(slope) * 100, 0.9)
            evidence.append(self._create_evidence(
                "trend",
                f"Positive regression slope on {tf} ({(slope * 100):.4f}%)",
                tf, strength, "bullish", "analyzer.trend"
            ))
        elif slope < 0:
            strength = min(abs(slope) * 100, 0.9)
            evidence.append(self._create_evidence(
                "trend",
                f"Negative regression slope on {tf} ({(slope * 100):.4f}%)",
                tf, strength, "bearish", "analyzer.trend"
            ))

        # 3. MACD
        macd = ind.compute_macd(closes)
        if macd["histogram"]:
            last_hist = macd["histogram"][-1]
            if last_hist > 0:
                evidence.append(self._create_evidence(
                    "trend",
                    f"MACD histogram positive on {tf} (bullish momentum)",
                    tf, 0.60, "bullish", "analyzer.trend"
                ))
            else:
                evidence.append(self._create_evidence(
                    "trend",
                    f"MACD histogram negative on {tf} (bearish momentum)",
                    tf, 0.60, "bearish", "analyzer.trend"
                ))

        return evidence

    def _analyze_volume(self, volumes: list[float], closes: list[float],
                        tf: str) -> list[MarketEvidence]:
        """Analyze volume: trend, spikes, divergence."""
        evidence: list[MarketEvidence] = []

        # 1. Volume trend
        vol_trend = ind.compute_volume_trend(volumes)
        if vol_trend == "increasing":
            evidence.append(self._create_evidence(
                "volume",
                f"Volume increasing on {tf} (conviction)",
                tf, 0.65, "bullish", "analyzer.volume"
            ))
        elif vol_trend == "decreasing":
            evidence.append(self._create_evidence(
                "volume",
                f"Volume decreasing on {tf} (low participation)",
                tf, 0.50, "neutral", "analyzer.volume"
            ))

        # 2. Volume spike
        vol_stats = ind.compute_volume_stats(volumes)
        if vol_stats["recent_avg"] > vol_stats["average"] * 2:
            evidence.append(self._create_evidence(
                "volume",
                f"Volume spike detected on {tf} ({vol_stats['recent_avg']:.0f} vs avg {vol_stats['average']:.0f})",
                tf, 0.70, "bullish", "analyzer.volume"
            ))

        # 3. Volume-price divergence (simple check)
        if len(closes) >= 20 and len(volumes) >= 20:
            price_up = closes[-1] > closes[-5]
            vol_up = sum(volumes[-5:]) > sum(volumes[-10:-5])
            if price_up and not vol_up:
                evidence.append(self._create_evidence(
                    "volume",
                    f"Weak volume on {tf} price advance (possible divergence)",
                    tf, 0.55, "bearish", "analyzer.volume"
                ))
            elif not price_up and vol_up:
                evidence.append(self._create_evidence(
                    "volume",
                    f"High volume on {tf} price decline (distribution)",
                    tf, 0.55, "bearish", "analyzer.volume"
                ))

        return evidence

    def _analyze_volatility(self, closes: list[float], highs: list[float],
                            lows: list[float], tf: str) -> list[MarketEvidence]:
        """Analyze volatility: ATR, Bollinger Bands."""
        evidence: list[MarketEvidence] = []

        # 1. ATR (volatility level)
        atr = ind.compute_atr(highs, lows, closes)
        if atr:
            current_price = closes[-1] if closes else 1
            atr_pct = (atr[-1] / current_price) * 100 if current_price > 0 else 0
            if atr_pct > 2:
                evidence.append(self._create_evidence(
                    "volatility",
                    f"High volatility on {tf} (ATR: {atr_pct:.2f}%)",
                    tf, min(atr_pct / 5, 0.9), "neutral", "analyzer.volatility"
                ))
            elif atr_pct < 0.5:
                evidence.append(self._create_evidence(
                    "volatility",
                    f"Low volatility on {tf} (ATR: {atr_pct:.2f}%)",
                    tf, 0.60, "neutral", "analyzer.volatility"
                ))

        # 2. Bollinger Bands
        bb = ind.compute_bollinger_bands(closes)
        if bb["upper"] and bb["lower"] and closes:
            current_price = closes[-1]
            bb_upper = bb["upper"][-1]
            bb_lower = bb["lower"][-1]
            bb_middle = bb["middle"][-1]
            bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle != 0 else 0
            if bb_width > 0.1:
                evidence.append(self._create_evidence(
                    "volatility",
                    f"Wide Bollinger Bands on {tf} (width: {bb_width:.2%})",
                    tf, min(bb_width * 5, 0.9), "neutral", "analyzer.volatility"
                ))
            elif bb_width < 0.02:
                evidence.append(self._create_evidence(
                    "volatility",
                    f"Narrow Bollinger Bands on {tf} (squeeze, width: {bb_width:.2%})",
                    tf, 0.70, "neutral", "analyzer.volatility"
                ))
            # Price touching bands
            if current_price >= bb_upper * 0.995:
                evidence.append(self._create_evidence(
                    "volatility",
                    f"Price touching upper Bollinger Band on {tf}",
                    tf, 0.65, "bearish", "analyzer.volatility"
                ))
            elif current_price <= bb_lower * 1.005:
                evidence.append(self._create_evidence(
                    "volatility",
                    f"Price touching lower Bollinger Band on {tf}",
                    tf, 0.65, "bullish", "analyzer.volatility"
                ))

        return evidence

    def get_analyzed_timeframes(self) -> list[str]:
        """Return list of timeframes that were analyzed."""
        return self._analyzed_timeframes
