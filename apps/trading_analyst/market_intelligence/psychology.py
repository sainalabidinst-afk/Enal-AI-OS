"""
Trading Psychology Analysis
===========================

Analyzes market sentiment and behavioral patterns:
- Fear and Greed indicators
- Market sentiment extremes
- Behavioral biases detection
- Crowd psychology patterns
- Risk tolerance assessment

This module produces observations about market psychology.
It does NOT produce trading signals.
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence, OHLCV

logger = logging.getLogger(__name__)


class PsychologyAnalyzer:
    """
    Analyze market psychology and sentiment.
    
    Detects:
    - Fear/Greed extremes (contrarian signals)
    - FOMO (Fear Of Missing Out) patterns
    - Capitulation (panic selling)
    - Euphoria (excessive bullishness)
    - Behavioral biases (confirmation, anchoring, recency)
    """

    def analyze_sentiment_extremes(self, rsi: float,
                                    volume_spike: bool,
                                    price_extreme: bool,
                                    tf: str) -> list[MarketEvidence]:
        """
        Detect sentiment extremes using RSI and price action.
        
        Args:
            rsi: Current RSI value (0-100)
            volume_spike: Whether volume is spiking
            price_extreme: Whether price is at extreme of range
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        # RSI extremes
        if rsi > 85:
            evidence.append(MarketEvidence(
                id=f"rsi_extreme_overbought_{tf}",
                type="psychology",
                description=f"RSI at {rsi:.1f} on {tf} - extreme overbought (euphoria risk)",
                timeframe=tf,
                strength=0.75,
                direction="bearish",
                source="psychology.sentiment_extremes",
                confidence=0.70,
            ))
            if volume_spike:
                evidence.append(MarketEvidence(
                    id=f"euphoria_blowoff_{tf}",
                    type="psychology",
                    description=f"RSI {rsi:.1f} + volume spike on {tf} - possible blowoff top (euphoria)",
                    timeframe=tf,
                    strength=0.85,
                    direction="bearish",
                    source="psychology.sentiment_extremes",
                    confidence=0.75,
                ))
        elif rsi < 15:
            evidence.append(MarketEvidence(
                id=f"rsi_extreme_oversold_{tf}",
                type="psychology",
                description=f"RSI at {rsi:.1f} on {tf} - extreme oversold (capitulation risk)",
                timeframe=tf,
                strength=0.75,
                direction="bullish",
                source="psychology.sentiment_extremes",
                confidence=0.70,
            ))
            if volume_spike:
                evidence.append(MarketEvidence(
                    id=f"capitulation_{tf}",
                    type="psychology",
                    description=f"RSI {rsi:.1f} + volume spike on {tf} - possible capitulation (panic selling)",
                    timeframe=tf,
                    strength=0.85,
                    direction="bullish",
                    source="psychology.sentiment_extremes",
                    confidence=0.75,
                ))
        elif rsi > 70:
            evidence.append(MarketEvidence(
                id=f"rsi_overbought_{tf}",
                type="psychology",
                description=f"RSI at {rsi:.1f} on {tf} - overbought (greed dominating)",
                timeframe=tf,
                strength=0.55,
                direction="bearish",
                source="psychology.sentiment_extremes",
                confidence=0.50,
            ))
        elif rsi < 30:
            evidence.append(MarketEvidence(
                id=f"rsi_oversold_{tf}",
                type="psychology",
                description=f"RSI at {rsi:.1f} on {tf} - oversold (fear dominating)",
                timeframe=tf,
                strength=0.55,
                direction="bullish",
                source="psychology.sentiment_extremes",
                confidence=0.50,
            ))

        # Price extreme + volume confirmation
        if price_extreme and volume_spike:
            evidence.append(MarketEvidence(
                id=f"climactic_action_{tf}",
                type="psychology",
                description=f"Price extreme + volume spike on {tf} - climactic behavior (emotional extreme)",
                timeframe=tf,
                strength=0.70,
                direction="neutral",
                source="psychology.sentiment_extremes",
                confidence=0.65,
            ))

        return evidence

    def analyze_fomo(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect FOMO (Fear Of Missing Out) patterns.
        
        FOMO indicators:
        - Consecutive large bullish candles
        - Volume increasing as price accelerates
        - Gaps (if applicable)
        - Price far from moving average
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 20:
            return evidence

        closes = [c.close for c in ohlcv]
        volumes = [c.volume for c in ohlcv]
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]

        # Check for accelerating price (consecutive large gains)
        recent_returns = []
        for i in range(max(0, len(closes) - 10), len(closes)):
            if i > 0 and closes[i - 1] > 0:
                ret = (closes[i] - closes[i - 1]) / closes[i - 1] * 100
                recent_returns.append(ret)

        if len(recent_returns) >= 5:
            consecutive_gains = 0
            for ret in recent_returns[-5:]:
                if ret > 1.0:  # >1% gain
                    consecutive_gains += 1
                else:
                    consecutive_gains = 0

            if consecutive_gains >= 3:
                vol_increasing = all(
                    volumes[-i] > volumes[-i - 1] for i in range(1, min(5, len(volumes)))
                ) if len(volumes) >= 5 else False

                if vol_increasing:
                    evidence.append(MarketEvidence(
                        id=f"fomo_acceleration_{tf}",
                        type="psychology",
                        description=f"FOMO pattern on {tf}: {consecutive_gains} large gains with increasing volume",
                        timeframe=tf,
                        strength=0.70,
                        direction="bearish",
                        source="psychology.fomo",
                        confidence=0.60,
                    ))
                else:
                    evidence.append(MarketEvidence(
                        id=f"fomo_weak_volume_{tf}",
                        type="psychology",
                        description=f"FOMO warning on {tf}: {consecutive_gains} large gains but volume not confirming",
                        timeframe=tf,
                        strength=0.55,
                        direction="bearish",
                        source="psychology.fomo",
                        confidence=0.50,
                    ))

            # Check for panic selling (consecutive large losses)
            consecutive_losses = 0
            for ret in recent_returns[-5:]:
                if ret < -1.0:  # >1% loss
                    consecutive_losses += 1
                else:
                    consecutive_losses = 0

            if consecutive_losses >= 3:
                vol_increasing = all(
                    volumes[-i] > volumes[-i - 1] for i in range(1, min(5, len(volumes)))
                ) if len(volumes) >= 5 else False

                if vol_increasing:
                    evidence.append(MarketEvidence(
                        id=f"panic_selling_{tf}",
                        type="psychology",
                        description=f"Panic selling on {tf}: {consecutive_losses} large losses with increasing volume",
                        timeframe=tf,
                        strength=0.75,
                        direction="bullish",
                        source="psychology.fomo",
                        confidence=0.65,
                    ))

        # Price far from 50-period MA (potential extreme)
        if len(closes) >= 50:
            sma50 = sum(closes[-50:]) / 50
            current_price = closes[-1]
            deviation = (current_price - sma50) / sma50 * 100

            if deviation > 15:
                evidence.append(MarketEvidence(
                    id=f"price_far_above_ma50_{tf}",
                    type="psychology",
                    description=f"Price {deviation:.1f}% above MA50 on {tf} - extended from mean (potential greed)",
                    timeframe=tf,
                    strength=min(deviation / 20, 0.85),
                    direction="bearish",
                    source="psychology.fomo",
                    confidence=0.65,
                ))
            elif deviation < -15:
                evidence.append(MarketEvidence(
                    id=f"price_far_below_ma50_{tf}",
                    type="psychology",
                    description=f"Price {abs(deviation):.1f}% below MA50 on {tf} - extended from mean (potential fear)",
                    timeframe=tf,
                    strength=min(abs(deviation) / 20, 0.85),
                    direction="bullish",
                    source="psychology.fomo",
                    confidence=0.65,
                ))

        return evidence

    def analyze_volume_psychology(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Analyze volume patterns for psychological insights.
        
        - High volume on up days vs down days (conviction)
        - Volume climax (exhaustion)
        - Low volume after trend (indecision)
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 20:
            return evidence

        volumes = [c.volume for c in ohlcv]
        closes = [c.close for c in ohlcv]

        # Volume on up vs down days
        up_volume = sum(
            volumes[i] for i in range(1, len(ohlcv))
            if closes[i] > closes[i - 1]
        )
        down_volume = sum(
            volumes[i] for i in range(1, len(ohlcv))
            if closes[i] < closes[i - 1]
        )
        total_volume = up_volume + down_volume

        if total_volume > 0:
            up_ratio = up_volume / total_volume

            if up_ratio > 0.7:
                evidence.append(MarketEvidence(
                    id=f"buying_conviction_{tf}",
                    type="psychology",
                    description=f"{up_ratio*100:.0f}% of volume on up days on {tf} - strong buying conviction",
                    timeframe=tf,
                    strength=min((up_ratio - 0.5) * 3, 0.85),
                    direction="bullish",
                    source="psychology.volume_psychology",
                    confidence=0.65,
                ))
            elif up_ratio < 0.3:
                evidence.append(MarketEvidence(
                    id=f"selling_conviction_{tf}",
                    type="psychology",
                    description=f"{down_volume/total_volume*100:.0f}% of volume on down days on {tf} - strong selling pressure",
                    timeframe=tf,
                    strength=min((0.5 - up_ratio) * 3, 0.85),
                    direction="bearish",
                    source="psychology.volume_psychology",
                    confidence=0.65,
                ))

        # Volume climax (highest volume in recent period)
        if len(volumes) >= 20:
            recent_volumes = volumes[-20:]
            avg_vol = sum(recent_volumes) / len(recent_volumes)
            max_vol = max(recent_volumes)
            vol_ratio = max_vol / avg_vol if avg_vol > 0 else 1

            if vol_ratio > 3:
                max_vol_idx = recent_volumes.index(max_vol)
                candle_idx = len(volumes) - 20 + max_vol_idx
                candle_close = closes[candle_idx] if candle_idx < len(closes) else 0
                prev_close = closes[candle_idx - 1] if candle_idx > 0 else 0

                if candle_close > prev_close:
                    evidence.append(MarketEvidence(
                        id=f"buying_climax_{tf}",
                        type="psychology",
                        description=f"Volume climax ({vol_ratio:.1f}x avg) on {tf} up day - potential buying exhaustion",
                        timeframe=tf,
                        strength=min(vol_ratio / 5, 0.85),
                        direction="bearish",
                        source="psychology.volume_psychology",
                        confidence=0.65,
                    ))
                else:
                    evidence.append(MarketEvidence(
                        id=f"selling_climax_{tf}",
                        type="psychology",
                        description=f"Volume climax ({vol_ratio:.1f}x avg) on {tf} down day - potential selling exhaustion",
                        timeframe=tf,
                        strength=min(vol_ratio / 5, 0.85),
                        direction="bullish",
                        source="psychology.volume_psychology",
                        confidence=0.65,
                    ))

        # Low volume after trend (indecision)
        if len(volumes) >= 30:
            recent_vol = sum(volumes[-10:]) / 10
            prior_vol = sum(volumes[-30:-10]) / 20
            vol_decline = recent_vol / prior_vol if prior_vol > 0 else 1

            if vol_decline < 0.5:
                evidence.append(MarketEvidence(
                    id=f"volume_quiet_{tf}",
                    type="psychology",
                    description=f"Volume dropped {((1 - vol_decline) * 100):.0f}% on {tf} - market indecision (waiting for catalyst)",
                    timeframe=tf,
                    strength=0.60,
                    direction="neutral",
                    source="psychology.volume_psychology",
                    confidence=0.55,
                ))

        return evidence

    def analyze(self, ohlcv: list[OHLCV], rsi: float, tf: str) -> list[MarketEvidence]:
        """Run full psychology analysis on a timeframe."""
        evidence: list[MarketEvidence] = []

        if not ohlcv or len(ohlcv) < 20:
            return evidence

        # Volume stats
        volumes = [c.volume for c in ohlcv]
        avg_vol = sum(volumes) / len(volumes) if volumes else 0
        recent_vol = sum(volumes[-5:]) / min(5, len(volumes)) if volumes else 0
        volume_spike = recent_vol > avg_vol * 2 if avg_vol > 0 else False

        # Price extreme check
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        current_price = ohlcv[-1].close if ohlcv else 0
        recent_high = max(highs[-20:]) if len(highs) >= 20 else max(highs)
        recent_low = min(lows[-20:]) if len(lows) >= 20 else min(lows)
        price_extreme = current_price > recent_high * 0.995 or current_price < recent_low * 1.005

        # Sentiment extremes
        evidence.extend(self.analyze_sentiment_extremes(rsi, volume_spike, price_extreme, tf))

        # FOMO patterns
        evidence.extend(self.analyze_fomo(ohlcv, tf))

        # Volume psychology
        evidence.extend(self.analyze_volume_psychology(ohlcv, tf))

        return evidence
