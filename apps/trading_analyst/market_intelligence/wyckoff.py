"""
Wyckoff Market Analysis
=======================

Implements Wyckoff Method concepts:
- Accumulation (Spring, SOS, LPS)
- Distribution (LPSY, SOW, UTAD)
- Composite Operator (CO) detection
- Supply/Demand analysis

Reference: Wyckoff Method by Richard D. Wyckoff
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence, OHLCV

logger = logging.getLogger(__name__)


class WyckoffAnalyzer:
    """
    Analyzes price/volume patterns using Wyckoff Method.
    
    Detects:
    - Accumulation phases (Spring, SOS, LPS)
    - Distribution phases (LPSY, SOW, UTAD)
    - Composite Operator behavior
    - Supply/Demand imbalance
    """

    def detect_accumulation(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect Wyckoff accumulation pattern.
        
        Typical accumulation:
        1. Preliminary Support (PS) after downtrend
        2. Selling Climax (SC) with high volume
        3. Automatic Rally (AR) on decreasing volume
        4. Secondary Test (ST) with lower volume
        5. Spring (final low shakeout)
        6. Sign of Strength (SOS) - breakout above resistance
        7. Last Point of Support (LPS) - pullback that holds
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 30:
            return evidence

        closes = [c.close for c in ohlcv]
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        volumes = [c.volume for c in ohlcv]
        current_price = closes[-1]

        # 1. Check for downtrend → sideways transition
        recent_high = max(highs[-10:])
        recent_low = min(lows[-10:])
        if recent_high > 0:
            recent_range = (recent_high - recent_low) / recent_high
        else:
            recent_range = 0

        # 2. Volume analysis: decreasing volume on lows
        recent_volumes = volumes[-20:]
        vol_avg = sum(recent_volumes) / len(recent_volumes) if recent_volumes else 0
        last_10_vol = sum(volumes[-10:]) / 10 if len(volumes) >= 10 else 0

        # 3. Spring detection: false breakdown below support
        if len(lows) >= 20:
            support_level = min(lows[-20:-5])
            current_low = lows[-5:]
            if min(current_low) < support_level and closes[-1] > support_level:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_spring_{tf}",
                    type="wyckoff",
                    description=f"Spring detected on {tf} - false breakdown below {support_level:.2f}",
                    timeframe=tf,
                    strength=0.75,
                    direction="bullish",
                    source="wyckoff.accumulation",
                    confidence=0.70,
                ))

        # 4. SOS (Sign of Strength) detection
        if len(highs) >= 15:
            recent_swing_high = max(highs[-15:-5])
            current_high = max(highs[-5:])
            current_vol = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else 0
            prev_vol = sum(volumes[-10:-5]) / 5 if len(volumes) >= 10 else 0
            
            if current_high > recent_swing_high and current_vol > prev_vol * 1.3:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_sos_{tf}",
                    type="wyckoff",
                    description=f"Sign of Strength (SOS) on {tf} - breakout above {recent_swing_high:.2f} with volume",
                    timeframe=tf,
                    strength=0.80,
                    direction="bullish",
                    source="wyckoff.accumulation",
                    confidence=0.75,
                ))

        # 5. Preliminary Support (PS) after downtrend
        if len(lows) >= 50:
            downtrend_lows = lows[-50:-20]
            downtrend_highs = highs[-50:-20]
            if max(downtrend_highs) < highs[-20] and min(downtrend_lows) > min(lows[-20:]):
                # Potential downtrend exhaustion
                vol_at_low = volumes[lows.index(min(lows[-20:]))]
                if vol_at_low > vol_avg * 1.5:
                    evidence.append(MarketEvidence(
                        id=f"wyckoff_ps_{tf}",
                        type="wyckoff",
                        description=f"Preliminary Support (PS) on {tf} - high volume at low",
                        timeframe=tf,
                        strength=0.65,
                        direction="bullish",
                        source="wyckoff.accumulation",
                        confidence=0.60,
                    ))

        # 6. Secondary Test (ST) with lower volume
        if len(volumes) >= 30:
            recent_vol_trend = sum(volumes[-10:]) / 10
            prior_vol = sum(volumes[-20:-10]) / 10
            if recent_vol_trend < prior_vol * 0.7 and current_price >= recent_low * 1.02:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_st_{tf}",
                    type="wyckoff",
                    description=f"Secondary Test (ST) on {tf} - lower volume at support",
                    timeframe=tf,
                    strength=0.70,
                    direction="bullish",
                    source="wyckoff.accumulation",
                    confidence=0.65,
                ))

        return evidence

    def detect_distribution(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect Wyckoff distribution pattern.
        
        Typical distribution:
        1. Preliminary Supply (PSY) after uptrend
        2. Buying Climax (BC) with high volume
        3. Automatic Reaction (AR) on decreasing volume
        4. Secondary Test (ST) with lower volume
        5. LPSY (Last Point of Supply)
        6. Sign of Weakness (SOW)
        7. Upthrust After Distribution (UTAD)
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 30:
            return evidence

        closes = [c.close for c in ohlcv]
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        volumes = [c.volume for c in ohlcv]
        current_price = closes[-1]

        # 1. Upthrust After Distribution (UTAD) - false breakout above resistance
        if len(highs) >= 20:
            resistance_level = max(highs[-20:-5])
            current_high = max(highs[-5:])
            if current_high > resistance_level * 1.01 and current_price < resistance_level:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_utad_{tf}",
                    type="wyckoff",
                    description=f"Upthrust After Distribution (UTAD) on {tf} - false breakout above {resistance_level:.2f}",
                    timeframe=tf,
                    strength=0.80,
                    direction="bearish",
                    source="wyckoff.distribution",
                    confidence=0.75,
                ))

        # 2. Sign of Weakness (SOW)
        if len(lows) >= 15:
            recent_swing_low = min(lows[-15:-5])
            current_low = min(lows[-5:])
            current_vol = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else 0
            prev_vol = sum(volumes[-10:-5]) / 5 if len(volumes) >= 10 else 0
            
            if current_low < recent_swing_low and current_vol > prev_vol * 1.3:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_sow_{tf}",
                    type="wyckoff",
                    description=f"Sign of Weakness (SOW) on {tf} - breakdown below {recent_swing_low:.2f} with volume",
                    timeframe=tf,
                    strength=0.80,
                    direction="bearish",
                    source="wyckoff.distribution",
                    confidence=0.75,
                ))

        # 3. Buying Climax (BC) - high volume at top
        if len(highs) >= 20 and len(volumes) >= 20:
            max_high_idx = highs.index(max(highs[-20:]))
            max_vol_idx = volumes.index(max(volumes[-20:]))
            if abs(max_high_idx - max_vol_idx) <= 3:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_bc_{tf}",
                    type="wyckoff",
                    description=f"Buying Climax (BC) on {tf} - high volume at price high",
                    timeframe=tf,
                    strength=0.70,
                    direction="bearish",
                    source="wyckoff.distribution",
                    confidence=0.65,
                ))

        # 4. LPSY (Last Point of Supply) - rally that fails
        if len(highs) >= 15:
            recent_decline = min(lows[-15:-5])
            bounce = max(highs[-5:])
            bounce_vol = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else 0
            decline_vol = sum(volumes[-15:-10]) / 5 if len(volumes) >= 15 else 0
            
            if bounce > recent_decline * 1.02 and bounce_vol < decline_vol * 0.7:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_lpsy_{tf}",
                    type="wyckoff",
                    description=f"Last Point of Supply (LPSY) on {tf} - weak rally",
                    timeframe=tf,
                    strength=0.70,
                    direction="bearish",
                    source="wyckoff.distribution",
                    confidence=0.65,
                ))

        return evidence

    def analyze_composite_operator(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Analyze Composite Operator (CO) behavior.
        
        The CO is the collective smart money that moves price.
        Look for:
        - Absorption: large positions being accumulated/distributed
        - Markup/Markdown phases
        - Re-accumulation/Re-distribution
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 50:
            return evidence

        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        volumes = [c.volume for c in ohlcv]

        # 1. Absorption detection: wide range + high volume + small price change
        recent_high = max(highs[-10:])
        recent_low = min(lows[-10:])
        if recent_low > 0:
            price_range = (recent_high - recent_low) / recent_low
        else:
            price_range = 0

        recent_vol_avg = sum(volumes[-10:]) / 10
        overall_vol_avg = sum(volumes) / len(volumes)

        if overall_vol_avg > 0 and recent_vol_avg > overall_vol_avg * 1.5 and price_range < 0.05:
            evidence.append(MarketEvidence(
                id=f"wyckoff_absorption_{tf}",
                type="wyckoff",
                description=f"Composite Operator absorption on {tf} - high volume, narrow range",
                timeframe=tf,
                strength=0.75,
                direction="neutral",
                source="wyckoff.composite_operator",
                confidence=0.70,
            ))

        # 2. Markup phase: consistent higher highs + higher lows
        if len(highs) >= 20:
            swing_highs_flag = all(highs[i] > highs[i-5] for i in range(-5, 0) if abs(i) <= len(highs))
            swing_lows_flag = all(lows[i] > lows[i-5] for i in range(-5, 0) if abs(i) <= len(lows))
            if swing_highs_flag and swing_lows_flag:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_markup_{tf}",
                    type="wyckoff",
                    description=f"Markup phase detected on {tf} - consistent Higher Highs and Higher Lows",
                    timeframe=tf,
                    strength=0.80,
                    direction="bullish",
                    source="wyckoff.composite_operator",
                    confidence=0.75,
                ))

        # 3. Markdown phase: consistent lower highs + lower lows
        if len(highs) >= 20:
            swing_highs_flag = all(highs[i] < highs[i-5] for i in range(-5, 0) if abs(i) <= len(highs))
            swing_lows_flag = all(lows[i] < lows[i-5] for i in range(-5, 0) if abs(i) <= len(lows))
            if swing_highs_flag and swing_lows_flag:
                evidence.append(MarketEvidence(
                    id=f"wyckoff_markdown_{tf}",
                    type="wyckoff",
                    description=f"Markdown phase detected on {tf} - consistent Lower Highs and Lower Lows",
                    timeframe=tf,
                    strength=0.80,
                    direction="bearish",
                    source="wyckoff.composite_operator",
                    confidence=0.75,
                ))

        return evidence

    def analyze(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """Run full Wyckoff analysis on a timeframe."""
        evidence = []
        evidence.extend(self.detect_accumulation(ohlcv, tf))
        evidence.extend(self.detect_distribution(ohlcv, tf))
        evidence.extend(self.analyze_composite_operator(ohlcv, tf))
        return evidence
