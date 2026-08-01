"""
Smart Money Concepts (SMC) Analysis
====================================

Implements SMC / ICT concepts:
- Market Structure (HH, HL, LH, LL)
- Fair Value Gap (FVG) detection
- Order Blocks (OB)
- Liquidity sweeps
- Premium/Discount zones
- Optimal Trade Entry (OTE)

Reference: ICT (Inner Circle Trader) concepts by Michael Huddleston
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence, OHLCV

logger = logging.getLogger(__name__)


class SMCAnalyzer:
    """
    Analyze market structure using Smart Money Concepts.
    
    Provides:
    - Market structure levels (HH, HL, LH, LL)
    - Fair Value Gaps (FVG)
    - Order Blocks (bullish/bearish)
    - Liquidity sweeps
    - Premium/Discount array
    - Optimal Trade Entry zones
    """

    def detect_fair_value_gaps(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect Fair Value Gaps (FVG).
        
        FVG occurs when three consecutive candles have a gap between
        candle 1's low and candle 3's high (bullish FVG) or
        candle 1's high and candle 3's low (bearish FVG).
        
        FVGs act as magnets - price tends to return to fill them.
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 4:
            return evidence

        for i in range(len(ohlcv) - 2):
            c1 = ohlcv[i]
            c2 = ohlcv[i + 1]
            c3 = ohlcv[i + 2]

            # Bullish FVG: c1 high < c3 low (gap up)
            if c1.high < c3.low:
                gap_size = c3.low - c1.high
                fvg_price = (c1.high + c3.low) / 2
                evidence.append(MarketEvidence(
                    id=f"fvg_bullish_{tf}_{i}",
                    type="smc_fvg",
                    description=f"Bullish FVG on {tf} at {fvg_price:.2f} (gap: {gap_size:.2f})",
                    timeframe=tf,
                    strength=min(gap_size / c1.high * 100, 0.9) if c1.high > 0 else 0.5,
                    direction="bullish",
                    source="smc.fvg",
                    confidence=0.65,
                ))

            # Bearish FVG: c1 low > c3 high (gap down)
            if c1.low > c3.high:
                gap_size = c1.low - c3.high
                fvg_price = (c1.low + c3.high) / 2
                evidence.append(MarketEvidence(
                    id=f"fvg_bearish_{tf}_{i}",
                    type="smc_fvg",
                    description=f"Bearish FVG on {tf} at {fvg_price:.2f} (gap: {gap_size:.2f})",
                    timeframe=tf,
                    strength=min(gap_size / c1.high * 100, 0.9) if c1.high > 0 else 0.5,
                    direction="bearish",
                    source="smc.fvg",
                    confidence=0.65,
                ))

        return evidence

    def detect_order_blocks(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect Order Blocks (OB).
        
        Bullish OB: Last down candle before strong up move
        Bearish OB: Last up candle before strong down move
        
        OBs act as support/resistance levels.
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 5:
            return evidence

        for i in range(2, len(ohlcv) - 2):
            c_prev = ohlcv[i - 1]
            c_curr = ohlcv[i]
            c_next = ohlcv[i + 1]
            c_next2 = ohlcv[i + 2]

            # Bullish OB: c_prev bearish, c_curr and c_next bullish
            if c_prev.close < c_prev.open and c_curr.close > c_prev.high and c_next.close > c_curr.high:
                ob_high = c_prev.high
                ob_low = c_prev.low
                evidence.append(MarketEvidence(
                    id=f"ob_bullish_{tf}_{i}",
                    type="smc_order_block",
                    description=f"Bullish Order Block on {tf} at {ob_low:.2f}-{ob_high:.2f}",
                    timeframe=tf,
                    strength=0.75,
                    direction="bullish",
                    source="smc.order_block",
                    confidence=0.70,
                ))

            # Bearish OB: c_prev bullish, c_curr and c_next bearish
            if c_prev.close > c_prev.open and c_curr.close < c_prev.low and c_next.close < c_curr.low:
                ob_high = c_prev.high
                ob_low = c_prev.low
                evidence.append(MarketEvidence(
                    id=f"ob_bearish_{tf}_{i}",
                    type="smc_order_block",
                    description=f"Bearish Order Block on {tf} at {ob_low:.2f}-{ob_high:.2f}",
                    timeframe=tf,
                    strength=0.75,
                    direction="bearish",
                    source="smc.order_block",
                    confidence=0.70,
                ))

        return evidence

    def detect_liquidity_sweeps(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect liquidity sweeps.
        
        Liquidity sweeps occur when price briefly breaks:
        - Above a previous high (to trigger buy stops) then reverses
        - Below a previous low (to trigger sell stops) then reverses
        
        These are also known as "stop hunts" or "liquidity grabs".
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 20:
            return evidence

        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        closes = [c.close for c in ohlcv]

        # 1. Liquidity sweep above recent high (bearish)
        if len(highs) >= 10:
            recent_high = max(highs[-10:-3])
            last_highs = highs[-3:]
            last_closes = closes[-3:]

            if max(last_highs) > recent_high and min(last_closes) < recent_high:
                sweep_high = max(last_highs)
                evidence.append(MarketEvidence(
                    id=f"liq_sweep_high_{tf}",
                    type="smc_liquidity",
                    description=f"Liquidity sweep above {recent_high:.2f} to {sweep_high:.2f} on {tf}",
                    timeframe=tf,
                    strength=0.80,
                    direction="bearish",
                    source="smc.liquidity",
                    confidence=0.75,
                ))

        # 2. Liquidity sweep below recent low (bullish)
        if len(lows) >= 10:
            recent_low = min(lows[-10:-3])
            last_lows = lows[-3:]
            last_closes = closes[-3:]

            if min(last_lows) < recent_low and max(last_closes) > recent_low:
                sweep_low = min(last_lows)
                evidence.append(MarketEvidence(
                    id=f"liq_sweep_low_{tf}",
                    type="smc_liquidity",
                    description=f"Liquidity sweep below {recent_low:.2f} to {sweep_low:.2f} on {tf}",
                    timeframe=tf,
                    strength=0.80,
                    direction="bullish",
                    source="smc.liquidity",
                    confidence=0.75,
                ))

        return evidence

    def detect_premium_discount_zones(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect Premium/Discount zones.
        
        Premium: Above 50% of range (sell zone)
        Discount: Below 50% of range (buy zone)
        Optimal Trade Entry (OTE): 70-80% discount/pullback
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 10:
            return evidence

        closes = [c.close for c in ohlcv]
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]
        current_price = closes[-1]

        # Calculate current range
        if len(highs) >= 20:
            range_high = max(highs[-20:])
            range_low = min(lows[-20:])
        else:
            range_high = max(highs)
            range_low = min(lows)

        if range_high == range_low:
            return evidence

        # Calculate position in range
        range_position = (current_price - range_low) / (range_high - range_low)

        if range_position > 0.788:
            evidence.append(MarketEvidence(
                id=f"premium_zone_{tf}",
                type="smc_fvg",
                description=f"Price in Premium zone on {tf} (78.8%+ of range) - sell zone",
                timeframe=tf,
                strength=0.70,
                direction="bearish",
                source="smc.premium_discount",
                confidence=0.65,
            ))
        elif range_position < 0.212:
            evidence.append(MarketEvidence(
                id=f"discount_zone_{tf}",
                type="smc_fvg",
                description=f"Price in Discount zone on {tf} (21.2%- of range) - buy zone",
                timeframe=tf,
                strength=0.70,
                direction="bullish",
                source="smc.premium_discount",
                confidence=0.65,
            ))

        # OTE (Optimal Trade Entry) zone: 70-80% pullback
        if 0.20 <= range_position <= 0.30 or 0.70 <= range_position <= 0.80:
            evidence.append(MarketEvidence(
                id=f"ote_zone_{tf}",
                type="smc_fvg",
                description=f"Optimal Trade Entry (OTE) zone on {tf}",
                timeframe=tf,
                strength=0.75,
                direction="neutral",
                source="smc.premium_discount",
                confidence=0.70,
            ))

        return evidence

    def analyze(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """Run full SMC analysis on a timeframe."""
        evidence = []
        evidence.extend(self.detect_fair_value_gaps(ohlcv, tf))
        evidence.extend(self.detect_order_blocks(ohlcv, tf))
        evidence.extend(self.detect_liquidity_sweeps(ohlcv, tf))
        evidence.extend(self.detect_premium_discount_zones(ohlcv, tf))
        return evidence
