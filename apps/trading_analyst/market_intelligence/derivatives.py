"""
Options & Futures Analysis
==========================

Analyzes derivatives market data for insights:
- Options: Greeks (Delta, Gamma, Theta, Vega, Rho), implied volatility,
  put/call ratio, IV skew, max pain, unusual activity
- Futures: contango/backwardation, basis, open interest, COT reports

This module produces factual observations about derivatives markets.
It does NOT produce trading signals.
"""

import logging
import math
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence

logger = logging.getLogger(__name__)


class DerivativesAnalyzer:
    """
    Analyze options and futures market data.
    
    Options Analysis:
    - Implied Volatility (IV) levels and changes
    - Put/Call ratio for sentiment
    - IV skew (volatility smile)
    - Max pain price level
    - Unusual activity detection
    
    Futures Analysis:
    - Contango/Backwardation regime
    - Basis (spot vs futures)
    - Open Interest trends
    - COT (Commitment of Traders) positioning
    """

    def analyze_iv(self, current_iv: float, historical_iv: float,
                   iv_percentile: float, tf: str = "1d") -> list[MarketEvidence]:
        """
        Analyze Implied Volatility.
        
        Args:
            current_iv: Current implied volatility (%)
            historical_iv: Historical average IV (%)
            iv_percentile: Current IV percentile (0-100)
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        if historical_iv == 0:
            return evidence

        iv_ratio = current_iv / historical_iv

        if iv_ratio > 1.5:
            evidence.append(MarketEvidence(
                id="iv_elevated",
                type="derivatives",
                description=f"IV at {current_iv:.1f}% - {(iv_ratio - 1) * 100:.0f}% above historical average "
                           f"(expensive options, expected volatility)",
                timeframe=tf,
                strength=min((iv_ratio - 1) * 0.8, 0.85),
                direction="neutral",
                source="derivatives.iv",
                confidence=0.70,
            ))
        elif iv_ratio < 0.5:
            evidence.append(MarketEvidence(
                id="iv_depressed",
                type="derivatives",
                description=f"IV at {current_iv:.1f}% - {(1 - iv_ratio) * 100:.0f}% below historical average "
                           f"(cheap options, complacency)",
                timeframe=tf,
                strength=min((1 - iv_ratio) * 0.8, 0.80),
                direction="neutral",
                source="derivatives.iv",
                confidence=0.65,
            ))

        if iv_percentile > 90:
            evidence.append(MarketEvidence(
                id="iv_high_percentile",
                type="derivatives",
                description=f"IV at {iv_percentile:.0f}th percentile - extreme fear pricing",
                timeframe=tf,
                strength=0.75,
                direction="bearish",
                source="derivatives.iv",
                confidence=0.70,
            ))
        elif iv_percentile < 10:
            evidence.append(MarketEvidence(
                id="iv_low_percentile",
                type="derivatives",
                description=f"IV at {iv_percentile:.0f}th percentile - extreme complacency",
                timeframe=tf,
                strength=0.70,
                direction="bullish",
                source="derivatives.iv",
                confidence=0.65,
            ))

        return evidence

    def analyze_put_call_ratio(self, put_volume: float, call_volume: float,
                                put_oi: float, call_oi: float,
                                tf: str = "1d") -> list[MarketEvidence]:
        """
        Analyze Put/Call ratio for sentiment.
        
        Args:
            put_volume: Total put option volume
            call_volume: Total call option volume
            put_oi: Total put open interest
            call_oi: Total call open interest
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        tot_vol = put_volume + call_volume
        if tot_vol == 0:
            return evidence

        pc_ratio_vol = put_volume / call_volume if call_volume > 0 else float('inf')
        pc_ratio_oi = put_oi / call_oi if call_oi > 0 else float('inf')

        # Volume ratio (short-term sentiment)
        if pc_ratio_vol > 1.5:
            evidence.append(MarketEvidence(
                id="pc_ratio_high_vol",
                type="derivatives",
                description=f"Put/Call volume ratio at {pc_ratio_vol:.2f} - bearish sentiment "
                           f"(puts dominating flow)",
                timeframe=tf,
                strength=min((pc_ratio_vol - 1) * 0.5, 0.80),
                direction="bearish",
                source="derivatives.put_call_ratio",
                confidence=0.65,
            ))
        elif pc_ratio_vol < 0.5:
            evidence.append(MarketEvidence(
                id="pc_ratio_low_vol",
                type="derivatives",
                description=f"Put/Call volume ratio at {pc_ratio_vol:.2f} - bullish sentiment "
                           f"(calls dominating flow)",
                timeframe=tf,
                strength=min((1 - pc_ratio_vol) * 0.5, 0.80),
                direction="bullish",
                source="derivatives.put_call_ratio",
                confidence=0.65,
            ))

        # Open Interest ratio (long-term positioning)
        if pc_ratio_oi > 1.2:
            evidence.append(MarketEvidence(
                id="pc_ratio_high_oi",
                type="derivatives",
                description=f"Put/Call OI ratio at {pc_ratio_oi:.2f} - defensive positioning "
                           f"(hedging dominant)",
                timeframe=tf,
                strength=min((pc_ratio_oi - 1) * 0.6, 0.75),
                direction="bearish",
                source="derivatives.put_call_ratio",
                confidence=0.60,
            ))
        elif pc_ratio_oi < 0.6:
            evidence.append(MarketEvidence(
                id="pc_ratio_low_oi",
                type="derivatives",
                description=f"Put/Call OI ratio at {pc_ratio_oi:.2f} - aggressive positioning "
                           f"(bullish bets dominant)",
                timeframe=tf,
                strength=min((1 - pc_ratio_oi) * 0.6, 0.75),
                direction="bullish",
                source="derivatives.put_call_ratio",
                confidence=0.60,
            ))

        # Divergence between volume and OI (unusual activity)
        if (pc_ratio_vol > 1.5 and pc_ratio_oi < 0.8) or \
           (pc_ratio_vol < 0.5 and pc_ratio_oi > 1.2):
            evidence.append(MarketEvidence(
                id="pc_ratio_divergence",
                type="derivatives",
                description=f"Put/Call divergence: volume ratio {pc_ratio_vol:.2f} vs OI ratio {pc_ratio_oi:.2f} "
                           f"- possible positioning shift",
                timeframe=tf,
                strength=0.65,
                direction="neutral",
                source="derivatives.put_call_ratio",
                confidence=0.55,
            ))

        return evidence

    def analyze_iv_skew(self, otm_put_iv: float, atm_iv: float,
                        otm_call_iv: float, tf: str = "1d") -> list[MarketEvidence]:
        """
        Analyze IV skew (volatility smile).
        
        Args:
            otm_put_iv: Out-of-the-money put IV (%)
            atm_iv: At-the-money IV (%)
            otm_call_iv: Out-of-the-money call IV (%)
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        if atm_iv == 0:
            return evidence

        put_skew = otm_put_iv / atm_iv
        call_skew = otm_call_iv / atm_iv

        if put_skew > 1.3:
            evidence.append(MarketEvidence(
                id="iv_skew_put_high",
                type="derivatives",
                description=f"Put skew at {put_skew:.2f} - OTM puts expensive "
                           f"(downside fear premium)",
                timeframe=tf,
                strength=min((put_skew - 1) * 0.6, 0.80),
                direction="bearish",
                source="derivatives.iv_skew",
                confidence=0.65,
            ))
        elif put_skew < 0.9:
            evidence.append(MarketEvidence(
                id="iv_skew_put_low",
                type="derivatives",
                description=f"Put skew at {put_skew:.2f} - OTM puts cheap "
                           f"(low downside fear)",
                timeframe=tf,
                strength=0.60,
                direction="bullish",
                source="derivatives.iv_skew",
                confidence=0.55,
            ))

        if call_skew > 1.3:
            evidence.append(MarketEvidence(
                id="iv_skew_call_high",
                type="derivatives",
                description=f"Call skew at {call_skew:.2f} - OTM calls expensive "
                           f"(upside optimism premium)",
                timeframe=tf,
                strength=min((call_skew - 1) * 0.6, 0.80),
                direction="bullish",
                source="derivatives.iv_skew",
                confidence=0.65,
            ))

        return evidence

    def analyze_futures_basis(self, spot_price: float, futures_price: float,
                              current_price: float,
                              tf: str = "1d") -> list[MarketEvidence]:
        """
        Analyze futures basis (spot vs futures).
        
        Args:
            spot_price: Current spot price
            futures_price: Current futures price
            current_price: Current market price
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        if spot_price == 0:
            return evidence

        basis = (futures_price - spot_price) / spot_price * 100
        annualized_basis = basis * 12  # Simplified monthly → annual

        if basis > 2:
            evidence.append(MarketEvidence(
                id="futures_contango",
                type="derivatives",
                description=f"Futures in contango: futures {futures_price:.2f} vs spot {spot_price:.2f} "
                           f"(basis: {basis:.2f}%, annualized: {annualized_basis:.1f}%)",
                timeframe=tf,
                strength=min(basis * 0.1, 0.75),
                direction="bearish",
                source="derivatives.futures_basis",
                confidence=0.60,
            ))
        elif basis < -2:
            evidence.append(MarketEvidence(
                id="futures_backwardation",
                type="derivatives",
                description=f"Futures in backwardation: futures {futures_price:.2f} vs spot {spot_price:.2f} "
                           f"(basis: {basis:.2f}%, annualized: {annualized_basis:.1f}%)",
                timeframe=tf,
                strength=min(abs(basis) * 0.1, 0.75),
                direction="bullish",
                source="derivatives.futures_basis",
                confidence=0.60,
            ))

        return evidence

    def analyze_cot(self, commercial_long: float, commercial_short: float,
                    large_spec_long: float, large_spec_short: float,
                    small_spec_long: float, small_spec_short: float,
                    open_interest: float, tf: str = "1w") -> list[MarketEvidence]:
        """
        Analyze COT (Commitment of Traders) report.
        
        Args:
            commercial_long: Commercial (hedger) long positions
            commercial_short: Commercial (hedger) short positions
            large_spec_long: Large speculator long positions
            large_spec_short: Large speculator short positions
            small_spec_long: Small speculator long positions
            small_spec_short: Small speculator short positions
            open_interest: Total open interest
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        tot_comm = commercial_long + commercial_short
        tot_large = large_spec_long + large_spec_short
        tot_small = small_spec_long + small_spec_short

        if tot_comm > 0 and tot_large > 0:
            # Commercial (smart money) net position
            comm_net = (commercial_long - commercial_short) / tot_comm * 100

            # Large speculator (dumb money) net position
            large_net = (large_spec_long - large_spec_short) / tot_large * 100

            # Commercial net long
            if comm_net > 15:
                evidence.append(MarketEvidence(
                    id="cot_commercial_long",
                    type="derivatives",
                    description=f"Commercials net long {comm_net:.0f}% - smart money bullish",
                    timeframe=tf,
                    strength=min(comm_net * 0.02, 0.80),
                    direction="bullish",
                    source="derivatives.cot",
                    confidence=0.65,
                ))
            elif comm_net < -15:
                evidence.append(MarketEvidence(
                    id="cot_commercial_short",
                    type="derivatives",
                    description=f"Commercials net short {abs(comm_net):.0f}% - smart money bearish",
                    timeframe=tf,
                    strength=min(abs(comm_net) * 0.02, 0.80),
                    direction="bearish",
                    source="derivatives.cot",
                    confidence=0.65,
                ))

            # Large speculator net (contrarian)
            if large_net > 20:
                evidence.append(MarketEvidence(
                    id="cot_large_spec_long",
                    type="derivatives",
                    description=f"Large specs net long {large_net:.0f}% - crowd bullish (contrarian signal)",
                    timeframe=tf,
                    strength=min(large_net * 0.015, 0.70),
                    direction="bearish",
                    source="derivatives.cot",
                    confidence=0.55,
                ))
            elif large_net < -20:
                evidence.append(MarketEvidence(
                    id="cot_large_spec_short",
                    type="derivatives",
                    description=f"Large specs net short {abs(large_net):.0f}% - crowd bearish (contrarian signal)",
                    timeframe=tf,
                    strength=min(abs(large_net) * 0.015, 0.70),
                    direction="bullish",
                    source="derivatives.cot",
                    confidence=0.55,
                ))

            # Commercial vs Speculator divergence (strongest signal)
            if comm_net > 10 and large_net < -10:
                evidence.append(MarketEvidence(
                    id="cot_smart_money_bullish",
                    type="derivatives",
                    description=f"Smart money bullish (commercials +{comm_net:.0f}%) vs crowd bearish "
                               f"(specs {large_net:.0f}%) - strong bullish divergence",
                    timeframe=tf,
                    strength=0.80,
                    direction="bullish",
                    source="derivatives.cot",
                    confidence=0.70,
                ))
            elif comm_net < -10 and large_net > 10:
                evidence.append(MarketEvidence(
                    id="cot_smart_money_bearish",
                    type="derivatives",
                    description=f"Smart money bearish (commercials {comm_net:.0f}%) vs crowd bullish "
                               f"(specs +{large_net:.0f}%) - strong bearish divergence",
                    timeframe=tf,
                    strength=0.80,
                    direction="bearish",
                    source="derivatives.cot",
                    confidence=0.70,
                ))

        return evidence

    def analyze_max_pain(self, option_chain: dict[str, Any],
                         current_price: float, tf: str = "1d") -> list[MarketEvidence]:
        """
        Analyze max pain (option expiration gravity).
        
        Simplified calculation: the price level where the most options
        would expire worthless.
        
        Args:
            option_chain: Dict with strikes, call_oi, put_oi
            current_price: Current market price
            tf: Timeframe
        """
        evidence: list[MarketEvidence] = []

        strikes = option_chain.get("strikes", [])
        call_oi_values = option_chain.get("call_oi", [])
        put_oi_values = option_chain.get("put_oi", [])

        if not strikes:
            return evidence

        # Simplified max pain: find strike closest to current price
        # with highest total OI
        max_pain = 0
        max_pain_value = 0

        for i, strike in enumerate(strikes):
            total_oi = 0
            if i < len(call_oi_values):
                total_oi += call_oi_values[i]
            if i < len(put_oi_values):
                total_oi += put_oi_values[i]

            if total_oi > max_pain_value:
                max_pain_value = total_oi
                max_pain = strike

        if max_pain > 0 and current_price > 0:
            dist_to_max_pain = (current_price - max_pain) / max_pain * 100

            if abs(dist_to_max_pain) < 1:
                evidence.append(MarketEvidence(
                    id="max_pain_proximity",
                    type="derivatives",
                    description=f"Price near max pain level ({max_pain:.2f}) - options gravity "
                               f"(distance: {abs(dist_to_max_pain):.2f}%)",
                    timeframe=tf,
                    strength=0.65,
                    direction="neutral",
                    source="derivatives.max_pain",
                    confidence=0.55,
                ))
            elif dist_to_max_pain > 3:
                evidence.append(MarketEvidence(
                    id="max_pain_above",
                    type="derivatives",
                    description=f"Price {dist_to_max_pain:.1f}% above max pain ({max_pain:.2f}) "
                               f"- potential pull to expiration",
                    timeframe=tf,
                    strength=min(dist_to_max_pain * 0.05, 0.70),
                    direction="bearish",
                    source="derivatives.max_pain",
                    confidence=0.50,
                ))
            elif dist_to_max_pain < -3:
                evidence.append(MarketEvidence(
                    id="max_pain_below",
                    type="derivatives",
                    description=f"Price {abs(dist_to_max_pain):.1f}% below max pain ({max_pain:.2f}) "
                               f"- potential rally to expiration",
                    timeframe=tf,
                    strength=min(abs(dist_to_max_pain) * 0.05, 0.70),
                    direction="bullish",
                    source="derivatives.max_pain",
                    confidence=0.50,
                ))

        return evidence

    def analyze(self, derivatives_data: dict[str, Any]) -> list[MarketEvidence]:
        """Run full derivatives analysis."""
        evidence: list[MarketEvidence] = []

        # IV analysis
        if "current_iv" in derivatives_data and "historical_iv" in derivatives_data:
            evidence.extend(self.analyze_iv(
                derivatives_data["current_iv"],
                derivatives_data["historical_iv"],
                derivatives_data.get("iv_percentile", 50),
            ))

        # Put/Call ratio
        if "put_volume" in derivatives_data and "call_volume" in derivatives_data:
            evidence.extend(self.analyze_put_call_ratio(
                derivatives_data["put_volume"],
                derivatives_data["call_volume"],
                derivatives_data.get("put_oi", 0),
                derivatives_data.get("call_oi", 0),
            ))

        # IV skew
        if all(k in derivatives_data for k in ["otm_put_iv", "atm_iv", "otm_call_iv"]):
            evidence.extend(self.analyze_iv_skew(
                derivatives_data["otm_put_iv"],
                derivatives_data["atm_iv"],
                derivatives_data["otm_call_iv"],
            ))

        # Futures basis
        if all(k in derivatives_data for k in ["spot_price", "futures_price"]):
            evidence.extend(self.analyze_futures_basis(
                derivatives_data["spot_price"],
                derivatives_data["futures_price"],
                derivatives_data.get("current_price", 0),
            ))

        # COT analysis
        cot_keys = ["commercial_long", "commercial_short", "large_spec_long",
                    "large_spec_short", "small_spec_long", "small_spec_short"]
        if all(k in derivatives_data for k in cot_keys):
            evidence.extend(self.analyze_cot(
                derivatives_data["commercial_long"],
                derivatives_data["commercial_short"],
                derivatives_data["large_spec_long"],
                derivatives_data["large_spec_short"],
                derivatives_data["small_spec_long"],
                derivatives_data["small_spec_short"],
                derivatives_data.get("open_interest", 0),
            ))

        # Max pain
        if "option_chain" in derivatives_data:
            evidence.extend(self.analyze_max_pain(
                derivatives_data["option_chain"],
                derivatives_data.get("current_price", 0),
            ))

        return evidence
