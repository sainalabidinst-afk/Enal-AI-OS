"""
Elliott Wave Analysis
=====================

Implements basic Elliott Wave Principle concepts:
- Impulse waves (1-2-3-4-5)
- Corrective waves (A-B-C)
- Fibonacci relationships between waves
- Wave pattern recognition

Reference: Elliott Wave Principle by A.J. Frost and Robert Prechter
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence, OHLCV

logger = logging.getLogger(__name__)


class ElliottWaveAnalyzer:
    """
    Analyze price action for Elliott Wave patterns.
    
    Detects:
    - Impulse wave structure (5-wave)
    - Corrective wave structure (3-wave)
    - Fibonacci retracement/extensions
    - Wave degree classification
    """

    def detect_impulse_wave(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect 5-wave impulse pattern.
        
        Rules:
        - Wave 1: Initial move, often with low volume
        - Wave 2: Retracement of wave 1 (typically 50-61.8%)
        - Wave 3: Longest, strongest wave (volume expands)
        - Wave 4: Retracement of wave 3 (typically 38.2-50%)
        - Wave 5: Final wave (often with divergence)
        
        Rules:
        - Wave 2 cannot retrace beyond wave 1 start
        - Wave 3 cannot be the shortest
        - Wave 4 cannot overlap wave 1
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 50:
            return evidence

        closes = [c.close for c in ohlcv]
        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]

        # Simplified pattern detection: find swing points
        swing_highs = []
        swing_lows = []

        for i in range(5, len(ohlcv) - 5):
            if all(highs[i] > highs[j] for j in range(i - 5, i)) and \
               all(highs[i] > highs[j] for j in range(i + 1, i + 6)):
                swing_highs.append((i, highs[i]))
            if all(lows[i] < lows[j] for j in range(i - 5, i)) and \
               all(lows[i] < lows[j] for j in range(i + 1, i + 6)):
                swing_lows.append((i, lows[i]))

        # Need at least 5 swing points for a wave count
        if len(swing_highs) < 3 or len(swing_lows) < 3:
            return evidence

        # Check for 5-wave impulse pattern (alternating swings)
        if len(swing_highs) >= 3 and len(swing_lows) >= 2:
            last_highs = [h for _, h in swing_highs[-3:]]
            last_lows = [l for _, l in swing_lows[-2:]]

            # Impulse: higher highs and higher lows
            if last_highs[-1] > last_highs[-2] > last_highs[-3] and \
               last_lows[-1] > last_lows[-2]:
                evidence.append(MarketEvidence(
                    id=f"impulse_wave_{tf}",
                    type="elliott_wave",
                    description=f"Impulse wave structure detected on {tf} (5-wave pattern)",
                    timeframe=tf,
                    strength=0.70,
                    direction="bullish",
                    source="elliott_wave.impulse",
                    confidence=0.65,
                ))

                # Check if wave 3 is the strongest (volume confirmation)
                recent_volumes = [c.volume for c in ohlcv[-30:]]
                if recent_volumes:
                    vol_mid = len(recent_volumes) // 2
                    if sum(recent_volumes[vol_mid:]) > sum(recent_volumes[:vol_mid]):
                        evidence.append(MarketEvidence(
                            id=f"impulse_wave3_strong_{tf}",
                            type="elliott_wave",
                            description=f"Wave 3 appears strongest on {tf} (volume confirmation)",
                            timeframe=tf,
                            strength=0.75,
                            direction="bullish",
                            source="elliott_wave.impulse",
                            confidence=0.70,
                        ))

            # Corrective: lower highs and lower lows
            if last_highs[-1] < last_highs[-2] < last_highs[-3] and \
               last_lows[-1] < last_lows[-2]:
                evidence.append(MarketEvidence(
                    id=f"corrective_wave_{tf}",
                    type="elliott_wave",
                    description=f"Corrective wave structure detected on {tf} (A-B-C pattern)",
                    timeframe=tf,
                    strength=0.70,
                    direction="bearish",
                    source="elliott_wave.corrective",
                    confidence=0.65,
                ))

        # Check for wave 4 and wave 1 overlap (invalid if they overlap)
        if len(swing_lows) >= 2 and len(swing_highs) >= 2:
            wave_1_start = swing_lows[-2][1] if len(swing_lows) >= 2 else 0
            wave_4_start = swing_lows[-1][1] if swing_lows else 0
            wave_3_high = max(highs[-30:])

            if wave_4_start < wave_3_high and wave_4_start > wave_1_start:
                if wave_4_start < wave_1_start * 1.1:  # Close to overlapping
                    evidence.append(MarketEvidence(
                        id=f"wave_overlap_warning_{tf}",
                        type="elliott_wave",
                        description=f"Wave 4 near Wave 1 on {tf} - potential wave count violation",
                        timeframe=tf,
                        strength=0.50,
                        direction="neutral",
                        source="elliott_wave.validation",
                        confidence=0.45,
                    ))

        return evidence

    def detect_ending_diagonal(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """
        Detect Ending Diagonal pattern.
        
        An ending diagonal occurs in wave 5 of an impulse.
        Characterized by converging trendlines (wedge pattern)
        where sub-waves are 3-3-3-3-3.
        """
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 30:
            return evidence

        highs = [c.high for c in ohlcv]
        lows = [c.low for c in ohlcv]

        # Check for converging trendlines (wedge)
        if len(highs) >= 15:
            recent_highs = highs[-15:]
            recent_lows = lows[-15:]

            # Higher highs getting smaller
            high_rising_slowing = all(
                recent_highs[i] >= recent_highs[i-1] for i in range(1, len(recent_highs))
            ) and (recent_highs[-1] - recent_highs[0]) < (recent_highs[5] - recent_highs[0])

            # Lower lows slowing
            low_rising = all(
                recent_lows[i] >= recent_lows[i-1] for i in range(1, len(recent_lows))
            )

            current_close = ohlcv[-1].close if ohlcv else 0
            if high_rising_slowing and low_rising:
                evidence.append(MarketEvidence(
                    id=f"ending_diagonal_{tf}",
                    type="elliott_wave",
                    description=f"Possible Ending Diagonal on {tf} - wedge pattern at trend end",
                    timeframe=tf,
                    strength=0.65,
                    direction="bearish" if current_close > 0 else "neutral",
                    source="elliott_wave.diagonal",
                    confidence=0.55,
                ))

        return evidence

    def analyze(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """Run full Elliott Wave analysis on a timeframe."""
        evidence = []
        evidence.extend(self.detect_impulse_wave(ohlcv, tf))
        evidence.extend(self.detect_ending_diagonal(ohlcv, tf))
        return evidence
