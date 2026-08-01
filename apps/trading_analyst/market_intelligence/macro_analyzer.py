"""
Macro Analysis Engine
=====================

Analyzes macroeconomic factors that influence market direction:
- Central bank policy (Fed, ECB, BOJ, etc.)
- Economic indicators (CPI, GDP, employment, PMI)
- Risk-on/risk-off sentiment
- Geopolitical events
- Intermarket analysis (DXY, yields, commodities)

This module produces factual observations about macro conditions.
It does NOT produce trading signals.
"""

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import MarketEvidence

logger = logging.getLogger(__name__)


class MacroAnalyzer:
    """
    Analyze macroeconomic conditions and their market impact.
    
    Evaluates:
    - Central bank policy stance (dovish/hawkish)
    - Economic health indicators
    - Risk sentiment regime
    - Intermarket relationships
    """

    def __init__(self):
        # Fed rate decision history (simplified reference)
        self.fed_rates = {
            "2024-12": 4.50,
            "2025-01": 4.50,
            "2025-03": 4.25,
            "2025-05": 4.00,
            "2025-06": 3.75,
            "2025-09": 3.50,
            "2025-12": 3.25,
        }

    def analyze_policy_rate(self, current_rate: float, 
                           previous_rate: float,
                           central_bank: str = "Fed") -> list[MarketEvidence]:
        """
        Analyze central bank interest rate policy.
        
        Args:
            current_rate: Current policy rate (%)
            previous_rate: Previous policy rate (%)
            central_bank: Central bank name (Fed, ECB, BOJ, BOE)
        """
        evidence: list[MarketEvidence] = []
        rate_change = current_rate - previous_rate

        if rate_change > 0:
            # Rate hike
            strength = min(abs(rate_change) * 2, 0.85)
            evidence.append(MarketEvidence(
                id=f"rate_hike_{central_bank.lower()}",
                type="macro",
                description=f"{central_bank} raised rates by {abs(rate_change):.2f}% to {current_rate:.2f}% (hawkish)",
                timeframe="1d",
                strength=strength,
                direction="bearish",
                source="macro_analyzer.policy_rate",
                confidence=0.80,
            ))
            # Rate hikes are typically bearish for equities/crypto
            if current_rate > 5.0:
                evidence.append(MarketEvidence(
                    id=f"restrictive_rate_{central_bank.lower()}",
                    type="macro",
                    description=f"{central_bank} rate at {current_rate:.2f}% - restrictive territory",
                    timeframe="1d",
                    strength=0.75,
                    direction="bearish",
                    source="macro_analyzer.policy_rate",
                    confidence=0.70,
                ))
        elif rate_change < 0:
            # Rate cut
            strength = min(abs(rate_change) * 2, 0.85)
            evidence.append(MarketEvidence(
                id=f"rate_cut_{central_bank.lower()}",
                type="macro",
                description=f"{central_bank} cut rates by {abs(rate_change):.2f}% to {current_rate:.2f}% (dovish)",
                timeframe="1d",
                strength=strength,
                direction="bullish",
                source="macro_analyzer.policy_rate",
                confidence=0.80,
            ))
            # Rate cuts are typically bullish for equities/crypto
            if current_rate < 2.0:
                evidence.append(MarketEvidence(
                    id=f"accommodative_rate_{central_bank.lower()}",
                    type="macro",
                    description=f"{central_bank} rate at {current_rate:.2f}% - accommodative territory",
                    timeframe="1d",
                    strength=0.70,
                    direction="bullish",
                    source="macro_analyzer.policy_rate",
                    confidence=0.65,
                ))
        else:
            evidence.append(MarketEvidence(
                id=f"rate_hold_{central_bank.lower()}",
                type="macro",
                description=f"{central_bank} held rates at {current_rate:.2f}% (neutral)",
                timeframe="1d",
                strength=0.40,
                direction="neutral",
                source="macro_analyzer.policy_rate",
                confidence=0.60,
            ))

        return evidence

    def analyze_inflation(self, cpi: float, core_cpi: float,
                         target: float = 2.0) -> list[MarketEvidence]:
        """
        Analyze inflation data.
        
        Args:
            cpi: Headline CPI (year-over-year %)
            core_cpi: Core CPI (year-over-year %)
            target: Central bank inflation target
        """
        evidence: list[MarketEvidence] = []

        # Headline CPI
        cpi_deviation = cpi - target
        if cpi_deviation > 1.0:
            evidence.append(MarketEvidence(
                id="cpi_high",
                type="macro",
                description=f"CPI at {cpi:.1f}% - well above {target:.0f}% target (inflationary pressure)",
                timeframe="1w",
                strength=min(abs(cpi_deviation) * 0.15, 0.85),
                direction="bearish",
                source="macro_analyzer.inflation",
                confidence=0.75,
            ))
        elif cpi_deviation < -0.5:
            evidence.append(MarketEvidence(
                id="cpi_low",
                type="macro",
                description=f"CPI at {cpi:.1f}% - below {target:.0f}% target (deflation risk)",
                timeframe="1w",
                strength=min(abs(cpi_deviation) * 0.15, 0.70),
                direction="bullish",
                source="macro_analyzer.inflation",
                confidence=0.65,
            ))
        else:
            evidence.append(MarketEvidence(
                id="cpi_on_target",
                type="macro",
                description=f"CPI at {cpi:.1f}% - near {target:.0f}% target (stable inflation)",
                timeframe="1w",
                strength=0.50,
                direction="neutral",
                source="macro_analyzer.inflation",
                confidence=0.60,
            ))

        # Core vs Headline spread
        spread = core_cpi - cpi
        if spread > 0.5:
            evidence.append(MarketEvidence(
                id="core_cpi_sticky",
                type="macro",
                description=f"Core CPI ({core_cpi:.1f}%) above headline ({cpi:.1f}%) - sticky inflation",
                timeframe="1w",
                strength=0.65,
                direction="bearish",
                source="macro_analyzer.inflation",
                confidence=0.60,
            ))

        return evidence

    def analyze_economic_health(self, gdp_growth: float,
                                unemployment: float,
                                pmi: float) -> list[MarketEvidence]:
        """
        Analyze overall economic health using GDP, unemployment, and PMI.
        
        Args:
            gdp_growth: GDP growth rate (annual %)
            unemployment: Unemployment rate (%)
            pmi: Manufacturing PMI (50 = neutral)
        """
        evidence: list[MarketEvidence] = []

        # GDP analysis
        if gdp_growth > 3.0:
            evidence.append(MarketEvidence(
                id="gdp_strong",
                type="macro",
                description=f"GDP growth at {gdp_growth:.1f}% - strong economic expansion",
                timeframe="1w",
                strength=0.75,
                direction="bullish",
                source="macro_analyzer.economic_health",
                confidence=0.70,
            ))
        elif gdp_growth < 1.0:
            evidence.append(MarketEvidence(
                id="gdp_weak",
                type="macro",
                description=f"GDP growth at {gdp_growth:.1f}% - economic slowdown risk",
                timeframe="1w",
                strength=0.70,
                direction="bearish",
                source="macro_analyzer.economic_health",
                confidence=0.65,
            ))

        # Unemployment (Sahm Rule simplified)
        if unemployment > 6.0:
            evidence.append(MarketEvidence(
                id="unemployment_high",
                type="macro",
                description=f"Unemployment at {unemployment:.1f}% - recession indicator",
                timeframe="1w",
                strength=0.80,
                direction="bearish",
                source="macro_analyzer.economic_health",
                confidence=0.75,
            ))
        elif unemployment < 4.0:
            evidence.append(MarketEvidence(
                id="unemployment_low",
                type="macro",
                description=f"Unemployment at {unemployment:.1f}% - tight labor market",
                timeframe="1w",
                strength=0.65,
                direction="bullish",
                source="macro_analyzer.economic_health",
                confidence=0.60,
            ))

        # PMI analysis
        if pmi > 55:
            evidence.append(MarketEvidence(
                id="pmi_expansion",
                type="macro",
                description=f"PMI at {pmi:.1f} - manufacturing expansion",
                timeframe="1w",
                strength=min((pmi - 50) * 0.03, 0.80),
                direction="bullish",
                source="macro_analyzer.economic_health",
                confidence=0.70,
            ))
        elif pmi < 45:
            evidence.append(MarketEvidence(
                id="pmi_contraction",
                type="macro",
                description=f"PMI at {pmi:.1f} - manufacturing contraction",
                timeframe="1w",
                strength=min((50 - pmi) * 0.03, 0.80),
                direction="bearish",
                source="macro_analyzer.economic_health",
                confidence=0.70,
            ))

        return evidence

    def analyze_risk_sentiment(self, vix: float,
                               dxy: float,
                               bond_yield_10y: float,
                               spy_performance_1m: float) -> list[MarketEvidence]:
        """
        Analyze risk-on/risk-off sentiment.
        
        Args:
            vix: VIX volatility index
            dxy: US Dollar Index
            bond_yield_10y: 10-year Treasury yield (%)
            spy_performance_1m: SPY 1-month performance (%)
        """
        evidence: list[MarketEvidence] = []

        # VIX - fear gauge
        if vix > 30:
            evidence.append(MarketEvidence(
                id="vix_high",
                type="macro",
                description=f"VIX at {vix:.1f} - extreme fear (risk-off regime)",
                timeframe="1d",
                strength=min((vix - 20) * 0.02, 0.90),
                direction="bearish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.80,
            ))
        elif vix < 15:
            evidence.append(MarketEvidence(
                id="vix_low",
                type="macro",
                description=f"VIX at {vix:.1f} - low fear (risk-on regime)",
                timeframe="1d",
                strength=0.65,
                direction="bullish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.65,
            ))

        # DXY - dollar strength
        if dxy > 105:
            evidence.append(MarketEvidence(
                id="dxy_strong",
                type="macro",
                description=f"DXY at {dxy:.1f} - strong dollar (bearish for risk assets)",
                timeframe="1d",
                strength=min((dxy - 100) * 0.02, 0.80),
                direction="bearish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.70,
            ))
        elif dxy < 95:
            evidence.append(MarketEvidence(
                id="dxy_weak",
                type="macro",
                description=f"DXY at {dxy:.1f} - weak dollar (bullish for risk assets)",
                timeframe="1d",
                strength=min((100 - dxy) * 0.02, 0.80),
                direction="bullish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.70,
            ))

        # Yield curve (simplified)
        if bond_yield_10y > 5.0:
            evidence.append(MarketEvidence(
                id="yield_high",
                type="macro",
                description=f"10Y yield at {bond_yield_10y:.2f}% - high rate environment",
                timeframe="1d",
                strength=0.70,
                direction="bearish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.65,
            ))

        # SPY momentum
        if spy_performance_1m > 5:
            evidence.append(MarketEvidence(
                id="spy_momentum_positive",
                type="macro",
                description=f"SPY up {spy_performance_1m:.1f}% in 1 month - positive equity momentum",
                timeframe="1d",
                strength=min(spy_performance_1m * 0.03, 0.80),
                direction="bullish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.65,
            ))
        elif spy_performance_1m < -5:
            evidence.append(MarketEvidence(
                id="spy_momentum_negative",
                type="macro",
                description=f"SPY down {abs(spy_performance_1m):.1f}% in 1 month - negative equity momentum",
                timeframe="1d",
                strength=min(abs(spy_performance_1m) * 0.03, 0.80),
                direction="bearish",
                source="macro_analyzer.risk_sentiment",
                confidence=0.65,
            ))

        return evidence

    def analyze(self, macro_data: dict[str, Any]) -> list[MarketEvidence]:
        """
        Run full macro analysis.
        
        Expected macro_data keys:
            - central_bank: str
            - current_rate: float
            - previous_rate: float
            - cpi: float
            - core_cpi: float
            - gdp_growth: float
            - unemployment: float
            - pmi: float
            - vix: float
            - dxy: float
            - bond_yield_10y: float
            - spy_performance_1m: float
        """
        evidence: list[MarketEvidence] = []

        # Policy rate analysis
        if "current_rate" in macro_data and "previous_rate" in macro_data:
            cb = macro_data.get("central_bank", "Fed")
            evidence.extend(self.analyze_policy_rate(
                macro_data["current_rate"],
                macro_data["previous_rate"],
                cb,
            ))

        # Inflation analysis
        if "cpi" in macro_data and "core_cpi" in macro_data:
            evidence.extend(self.analyze_inflation(
                macro_data["cpi"],
                macro_data["core_cpi"],
            ))

        # Economic health
        if all(k in macro_data for k in ["gdp_growth", "unemployment", "pmi"]):
            evidence.extend(self.analyze_economic_health(
                macro_data["gdp_growth"],
                macro_data["unemployment"],
                macro_data["pmi"],
            ))

        # Risk sentiment
        if all(k in macro_data for k in ["vix", "dxy", "bond_yield_10y", "spy_performance_1m"]):
            evidence.extend(self.analyze_risk_sentiment(
                macro_data["vix"],
                macro_data["dxy"],
                macro_data["bond_yield_10y"],
                macro_data["spy_performance_1m"],
            ))

        return evidence
