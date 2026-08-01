"""
Volume Profile Analysis
=======================

Implements Volume Profile concepts:
- Point of Control (POC): price level with highest volume
- Value Area (VA): price range containing 70% of total volume
- High Volume Node (HVN): areas of high trading activity (support/resistance)
- Low Volume Node (LVN): areas of low trading activity (potential gaps)
- Volume profile structure: P shape, D shape, b shape, etc.

Volume Profile differs from traditional volume analysis because it
organizes volume by price level, not by time.
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence, OHLCV

logger = logging.getLogger(__name__)


class VolumeProfileAnalyzer:
    """
    Analyze volume by price level to identify key trading areas.
    
    Volume Profile reveals:
    - Where smart money accumulated/distributed
    - Fair value areas (POC ± Value Area)
    - Potential support/resistance levels
    - Price levels where institutional interest exists
    """

    def __init__(self, num_bins: int = 24):
        self.num_bins = num_bins

    def _build_profile(self, ohlcv: list[OHLCV]) -> dict[str, Any]:
        """
        Build volume profile from OHLCV data.
        
        Distributes volume across price levels using simple approximation:
        - Each candle's volume is distributed evenly across its range
        - Accumulates volume by price bin
        """
        if not ohlcv:
            return {"bins": {}, "poc": 0, "value_area_high": 0, "value_area_low": 0}

        # Find overall price range
        all_highs = [c.high for c in ohlcv]
        all_lows = [c.low for c in ohlcv]
        price_min = min(all_lows)
        price_max = max(all_highs)
        price_range = price_max - price_min

        if price_range == 0:
            return {"bins": {}, "poc": price_min, "value_area_high": price_min, "value_area_low": price_min}

        bin_size = price_range / self.num_bins

        # Initialize bins
        bins: dict[int, float] = {}
        for i in range(self.num_bins):
            bins[i] = 0.0

        # Distribute volume across bins
        total_volume = 0.0
        for candle in ohlcv:
            candle_low = candle.low
            candle_high = candle.high
            candle_volume = candle.volume
            candle_range = max(candle_high - candle_low, 0.001)

            # Find which bins this candle spans
            low_bin = int((candle_low - price_min) / bin_size)
            high_bin = int((candle_high - price_min) / bin_size)
            low_bin = max(0, min(low_bin, self.num_bins - 1))
            high_bin = max(0, min(high_bin, self.num_bins - 1))

            if low_bin == high_bin:
                bins[low_bin] += candle_volume
            else:
                # Distribute volume proportionally
                volume_per_unit = candle_volume / candle_range
                for bin_idx in range(low_bin, high_bin + 1):
                    bin_low = price_min + bin_idx * bin_size
                    bin_high = bin_low + bin_size
                    overlap_low = max(candle_low, bin_low)
                    overlap_high = min(candle_high, bin_high)
                    overlap = max(0, overlap_high - overlap_low)
                    bins[bin_idx] += overlap * volume_per_unit

            total_volume += candle_volume

        # Find POC (Point of Control) - bin with highest volume
        poc_bin = max(bins, key=lambda k: bins[k]) if bins else 0
        poc_price = price_min + (poc_bin + 0.5) * bin_size

        # Find Value Area (VA) - bins containing 70% of total volume around POC
        value_area_volume = total_volume * 0.70
        va_volume = 0.0
        va_low_bin = poc_bin
        va_high_bin = poc_bin
        expanding = True

        while expanding:
            # Try to expand to next lower bin
            lower_candidate = va_low_bin - 1
            higher_candidate = va_high_bin + 1

            lower_vol = bins.get(lower_candidate, 0) if lower_candidate >= 0 else -1
            higher_vol = bins.get(higher_candidate, 0) if higher_candidate < self.num_bins else -1

            if lower_vol < 0 and higher_vol < 0:
                expanding = False
            elif lower_vol >= higher_vol:
                va_low_bin = lower_candidate
                va_volume += lower_vol
            else:
                va_high_bin = higher_candidate
                va_volume += higher_vol

            if va_volume >= value_area_volume:
                expanding = False

        va_low_price = price_min + max(0, va_low_bin) * bin_size
        va_high_price = price_min + min(self.num_bins - 1, va_high_bin + 1) * bin_size

        # Identify HVN (High Volume Nodes) - bins with > 80% of POC volume
        poc_volume = bins[poc_bin] if poc_bin in bins else 0
        hvn_threshold = poc_volume * 0.8
        hvn_levels = []
        for bin_idx in sorted(bins.keys()):
            if bins[bin_idx] >= hvn_threshold:
                level_price = price_min + (bin_idx + 0.5) * bin_size
                hvn_levels.append(level_price)

        # Identify LVN (Low Volume Nodes) - bins with < 20% of POC volume
        lvn_threshold = poc_volume * 0.2
        lvn_levels = []
        for bin_idx in sorted(bins.keys()):
            if bins[bin_idx] < lvn_threshold and bins[bin_idx] > 0:
                level_price = price_min + (bin_idx + 0.5) * bin_size
                lvn_levels.append(level_price)

        # Determine profile shape
        # P shape: POC near top of VA, suggests selling pressure
        # D shape: POC near bottom of VA, suggests buying pressure
        # b shape: POC in middle, balanced
        va_range = va_high_price - va_low_price
        if va_range > 0:
            poc_position = (poc_price - va_low_price) / va_range
            if poc_position > 0.7:
                shape = "P"  # POC at top (selling pressure)
            elif poc_position < 0.3:
                shape = "b"  # POC at bottom (buying pressure)
            else:
                shape = "D"  # POC in middle (balanced, normal distribution)
        else:
            shape = "flat"

        return {
            "bins": {str(k): round(v, 2) for k, v in bins.items()},
            "poc_price": poc_price,
            "poc_volume": poc_volume,
            "value_area_high": va_high_price,
            "value_area_low": va_low_price,
            "value_area_volume_pct": (va_volume / total_volume * 100) if total_volume > 0 else 0,
            "hvn_levels": hvn_levels,
            "lvn_levels": lvn_levels,
            "shape": shape,
            "total_volume": total_volume,
            "bin_size": bin_size,
        }

    def analyze(self, ohlcv: list[OHLCV], tf: str) -> list[MarketEvidence]:
        """Run full Volume Profile analysis on a timeframe."""
        evidence: list[MarketEvidence] = []
        if len(ohlcv) < 30:
            return evidence

        profile = self._build_profile(ohlcv)
        if not profile or not profile.get("bins"):
            return evidence

        current_price = ohlcv[-1].close if ohlcv else 0
        poc = profile["poc_price"]
        va_high = profile["value_area_high"]
        va_low = profile["value_area_low"]

        # 1. Price relative to POC
        if current_price > 0 and poc > 0:
            dist_from_poc = (current_price - poc) / poc * 100
            if abs(dist_from_poc) < 0.5:
                evidence.append(MarketEvidence(
                    id=f"poc_proximity_{tf}",
                    type="volume_profile",
                    description=f"Price at Point of Control ({poc:.2f}) on {tf}",
                    timeframe=tf,
                    strength=0.80,
                    direction="neutral",
                    source="volume_profile.poc",
                    confidence=0.75,
                ))
            elif dist_from_poc > 2:
                evidence.append(MarketEvidence(
                    id=f"price_above_poc_{tf}",
                    type="volume_profile",
                    description=f"Price above POC ({poc:.2f}) on {tf} by {dist_from_poc:.1f}%",
                    timeframe=tf,
                    strength=min(dist_from_poc / 5, 0.85),
                    direction="bullish",
                    source="volume_profile.poc",
                    confidence=0.70,
                ))
            elif dist_from_poc < -2:
                evidence.append(MarketEvidence(
                    id=f"price_below_poc_{tf}",
                    type="volume_profile",
                    description=f"Price below POC ({poc:.2f}) on {tf} by {abs(dist_from_poc):.1f}%",
                    timeframe=tf,
                    strength=min(abs(dist_from_poc) / 5, 0.85),
                    direction="bearish",
                    source="volume_profile.poc",
                    confidence=0.70,
                ))

        # 2. Value Area boundaries as support/resistance
        if current_price > 0:
            dist_to_va_high = abs(current_price - va_high) / current_price * 100
            dist_to_va_low = abs(current_price - va_low) / current_price * 100

            if dist_to_va_high < 0.5:
                evidence.append(MarketEvidence(
                    id=f"va_high_proximity_{tf}",
                    type="volume_profile",
                    description=f"Price at Value Area high ({va_high:.2f}) on {tf} (resistance)",
                    timeframe=tf,
                    strength=0.75,
                    direction="bearish",
                    source="volume_profile.value_area",
                    confidence=0.70,
                ))
            if dist_to_va_low < 0.5:
                evidence.append(MarketEvidence(
                    id=f"va_low_proximity_{tf}",
                    type="volume_profile",
                    description=f"Price at Value Area low ({va_low:.2f}) on {tf} (support)",
                    timeframe=tf,
                    strength=0.75,
                    direction="bullish",
                    source="volume_profile.value_area",
                    confidence=0.70,
                ))

        # 3. Profile shape interpretation
        shape = profile.get("shape", "flat")
        if shape == "P":
            evidence.append(MarketEvidence(
                id=f"profile_shape_P_{tf}",
                type="volume_profile",
                description=f"P-shaped profile on {tf} - POC at top (selling pressure, potential rejection)",
                timeframe=tf,
                strength=0.65,
                direction="bearish",
                source="volume_profile.shape",
                confidence=0.60,
            ))
        elif shape == "b":
            evidence.append(MarketEvidence(
                id=f"profile_shape_b_{tf}",
                type="volume_profile",
                description=f"b-shaped profile on {tf} - POC at bottom (buying pressure, potential support)",
                timeframe=tf,
                strength=0.65,
                direction="bullish",
                source="volume_profile.shape",
                confidence=0.60,
            ))

        # 4. HVN/LVN levels near current price
        hvn_levels = profile.get("hvn_levels", [])
        lvn_levels = profile.get("lvn_levels", [])

        for hvn in hvn_levels[:3]:
            dist = abs(current_price - hvn) / current_price * 100 if current_price > 0 else 0
            if dist < 1:
                evidence.append(MarketEvidence(
                    id=f"hvn_proximity_{tf}_{hvn:.0f}",
                    type="volume_profile",
                    description=f"High Volume Node at {hvn:.2f} on {tf} (strong support/resistance)",
                    timeframe=tf,
                    strength=0.70,
                    direction="neutral",
                    source="volume_profile.hvn",
                    confidence=0.65,
                ))

        for lvn in lvn_levels[:3]:
            dist = abs(current_price - lvn) / current_price * 100 if current_price > 0 else 0
            if dist < 1:
                evidence.append(MarketEvidence(
                    id=f"lvn_proximity_{tf}_{lvn:.0f}",
                    type="volume_profile",
                    description=f"Low Volume Node at {lvn:.2f} on {tf} (potential gap fill)",
                    timeframe=tf,
                    strength=0.60,
                    direction="neutral",
                    source="volume_profile.lvn",
                    confidence=0.55,
                ))

        return evidence
