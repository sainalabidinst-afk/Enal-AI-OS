"""
Innovation Strategist — Strategy Analysis module.
"""

from __future__ import annotations

import hashlib
import logging

from apps.innovation_strategist.schemas import (
    BusinessContext,
    CompetitiveInsight,
    Competitor,
    InnovationConfig,
    InnovationOpportunity,
    Scenario,
    ScenarioLikelihood,
    TechnologyDomain,
    TechnologyForecast,
    TrendCategory,
    TrendDataPoint,
    TrendImpact,
    TrendSignal,
    TrendTimeframe,
)

logger = logging.getLogger(__name__)


class StrategyAnalysisEngine:
    """
    Provides trend analysis, technology forecasting, competitive intelligence,
    and scenario planning for strategic foresight.
    """

    CATEGORY_ADOPTION_BASE: dict[TrendCategory, float] = {
        TrendCategory.emerging_technology: 0.15,
        TrendCategory.market_dynamics: 0.45,
        TrendCategory.regulatory_change: 0.30,
        TrendCategory.consumer_behavior: 0.60,
        TrendCategory.sustainability: 0.35,
    }

    GROWTH_RATES: dict[TrendCategory, float] = {
        TrendCategory.emerging_technology: 0.65,
        TrendCategory.market_dynamics: 0.15,
        TrendCategory.regulatory_change: 0.10,
        TrendCategory.consumer_behavior: 0.25,
        TrendCategory.sustainability: 0.40,
    }

    def analyze_trends(self, config: InnovationConfig) -> list[TrendSignal]:
        """Analyze technology and market trends across configured categories."""
        signals = []
        for domain in config.technology_domains:
            for category in config.trend_categories:
                base_adoption = self.CATEGORY_ADOPTION_BASE.get(category, 0.3)
                growth = self.GROWTH_RATES.get(category, 0.2)
                historical = config.historical_trends.get(domain.name)
                current_adoption = self._compute_current_adoption(historical, base_adoption)
                growth_rate = growth + (len(historical) / 100.0) if historical else growth

                impact = self._classify_impact(domain, category)
                timeframe = self._classify_timeframe(category)
                confidence = min(1.0, round(0.7 + (current_adoption * 0.2), 2))

                signal_id = hashlib.md5(
                    f"{domain.name}-{category.value}".encode()
                ).hexdigest()[:8]

                signals.append(TrendSignal(
                    id=signal_id,
                    name=f"{domain.name} in {category.value}",
                    category=category,
                    description=(
                        f"Analysis of {domain.name} within "
                        f"{category.value.replace('_', ' ')}"
                    ),
                    impact=impact,
                    timeframe=timeframe,
                    current_adoption=current_adoption,
                    growth_rate=round(growth_rate, 4),
                    evidence=self._gather_evidence(domain, category),
                    confidence=confidence,
                ))
        return signals

    def forecast_technology(
        self, config: InnovationConfig, context: BusinessContext
    ) -> list[TechnologyForecast]:
        """Generate technology adoption forecasts using curve estimation."""
        forecasts = []
        for domain in config.technology_domains:
            adoption_curve = self._build_adoption_curve(domain, config.time_horizon)
            peak, mainstream, plateau = self._compute_timeframe(
                domain, config.time_horizon
            )

            forecast = TechnologyForecast(
                technology=domain.name,
                domain=domain.description,
                adoption_curve=adoption_curve,
                peak_year=peak,
                mainstream_year=mainstream,
                plateau_year=plateau,
                risk_factors=self._identify_tech_risks(domain),
                confidence=min(1.0, round(0.80 - (len(domain.name) / 100.0), 2)),
            )
            forecasts.append(forecast)
        return forecasts

    def analyze_competition(self, config: InnovationConfig) -> list[CompetitiveInsight]:
        """Analyze competitor positioning and market dynamics."""
        insights = []
        for competitor in config.competitors:
            insight = CompetitiveInsight(
                competitor=competitor.name,
                strength=competitor.strengths[0] if competitor.strengths else "Unknown",
                weakness=competitor.weaknesses[0] if competitor.weaknesses else "Unknown",
                market_position=self._market_position(competitor.market_share),
                threat_level=self._threat_level(competitor.market_share),
                opportunity=self._opportunity_from_weakness(competitor),
            )
            insights.append(insight)
        return insights

    def plan_scenarios(
        self, config: InnovationConfig, signals: list[TrendSignal]
    ) -> list[Scenario]:
        """Generate strategic scenarios based on trend signals."""
        scenarios = []
        high_impact = [
            s for s in signals
            if s.impact in (TrendImpact.transformative, TrendImpact.high)
        ]
        if not high_impact and signals:
            high_impact = signals[:3]

        for i, signal in enumerate(high_impact[:4]):
            likelihood = self._scenario_likelihood(signal)
            scenarios.append(Scenario(
                name=f"Scenario {i + 1}: {signal.name}",
                description=f"Impact of {signal.name} on {context_domain_placeholder(signal)}",
                likelihood=likelihood,
                impact=signal.impact,
                probability_score=round(signal.confidence * 0.8, 2),
                key_drivers=[signal.name, signal.category.value],
                implications=self._scenario_implications(signal),
                recommended_actions=self._scenario_actions(signal),
            ))

        # Always include a baseline scenario.
        scenarios.append(Scenario(
            name="Baseline: Business as Usual",
            description="Current trajectory continues with moderate innovation",
            likelihood=ScenarioLikelihood.likely,
            impact=TrendImpact.medium,
            probability_score=0.7,
            key_drivers=["market stability", "incremental innovation"],
            implications=["Gradual market share shifts", "Moderate technology adoption"],
            recommended_actions=["Maintain R&D investment", "Monitor trend signals"],
        ))
        return scenarios

    def identify_opportunities(
        self, config: InnovationConfig, signals: list[TrendSignal]
    ) -> list[InnovationOpportunity]:
        """Identify innovation opportunities from trend signals."""
        opportunities = []
        for signal in signals:
            if signal.impact in (TrendImpact.transformative, TrendImpact.high):
                opportunities.append(InnovationOpportunity(
                    title=f"Leverage {signal.name}",
                    description=(
                        f"Capitalize on {signal.category.value} trend "
                        f"with {signal.growth_rate} growth rate"
                    ),
                    trend_ids=[signal.id],
                    potential_value=signal.current_adoption * 1_000_000,
                    implementation_effort=(
                        TrendImpact.medium
                        if signal.timeframe == TrendTimeframe.short_term
                        else TrendImpact.high
                    ),
                    time_to_market=signal.timeframe,
                    confidence=signal.confidence,
                ))
        return opportunities

    def generate_narrative(
        self,
        signals: list[TrendSignal],
        forecasts: list[TechnologyForecast],
        scenarios: list[Scenario],
        opportunities: list[InnovationOpportunity],
    ) -> str:
        """Generate a strategic narrative from analysis components."""
        high_impact = [
            s for s in signals
            if s.impact in (TrendImpact.transformative, TrendImpact.high)
        ]
        return (
            f"Analysis identified {len(signals)} trend signals, "
            f"{len(forecasts)} technology forecasts, "
            f"{len(scenarios)} strategic scenarios, and "
            f"{len(opportunities)} innovation opportunities. "
            f"{len(high_impact)} high-impact trends require immediate attention. "
            f"Recommended focus: prioritize transformative trends with high growth potential."
        )

    def _compute_current_adoption(
        self, historical: list[TrendDataPoint] | None, base: float
    ) -> float:
        """Compute current adoption level from historical data or base value."""
        if not historical:
            return round(base, 4)
        values = [p.value for p in historical]
        return round(min(values[-1] / max(values[-1], 1.0), 1.0), 4) if values else base

    def _classify_impact(self, domain: TechnologyDomain, category: TrendCategory) -> TrendImpact:
        """Classify trend impact based on domain and category."""
        if category == TrendCategory.emerging_technology and domain.maturity_level == "emerging":
            return TrendImpact.transformative
        if category == TrendCategory.market_dynamics:
            return TrendImpact.high
        return TrendImpact.medium

    def _classify_timeframe(self, category: TrendCategory) -> TrendTimeframe:
        """Classify trend timeframe based on category."""
        mapping = {
            TrendCategory.emerging_technology: TrendTimeframe.long_term,
            TrendCategory.market_dynamics: TrendTimeframe.medium_term,
            TrendCategory.regulatory_change: TrendTimeframe.short_term,
            TrendCategory.consumer_behavior: TrendTimeframe.medium_term,
            TrendCategory.sustainability: TrendTimeframe.long_term,
        }
        return mapping.get(category, TrendTimeframe.medium_term)

    def _gather_evidence(self, domain: TechnologyDomain, category: TrendCategory) -> list[str]:
        """Gather evidence items for a trend signal."""
        return [
            f"Industry reports indicate {domain.name} growth in {category.value}",
            f"Research publications increasing for {domain.name}",
            f"Venture capital investment rising in {category.value}",
        ]

    def _build_adoption_curve(
        self, domain: TechnologyDomain, time_horizon: TrendTimeframe
    ) -> dict[str, float]:
        """Build a Gartner-style Hype Cycle adoption curve."""
        base = {
            "2026": 0.05, "2027": 0.15, "2028": 0.35,
            "2029": 0.55, "2030": 0.75, "2031": 0.88,
        }
        if time_horizon == TrendTimeframe.short_term:
            return {"2026": 0.15, "2027": 0.30, "2028": 0.45}
        if time_horizon == TrendTimeframe.long_term:
            return {**base, "2032": 0.95, "2033": 1.0}
        return base

    def _compute_timeframe(
        self, domain: TechnologyDomain, time_horizon: TrendTimeframe
    ) -> tuple[int, int, int]:
        """Compute peak, mainstream, and plateau years for a technology."""
        base_year = 2026
        offset = 0 if time_horizon == TrendTimeframe.short_term else (
            3 if time_horizon == TrendTimeframe.medium_term else 5
        )
        return (base_year + offset + 2, base_year + offset + 5, base_year + offset + 10)

    def _identify_tech_risks(self, domain: TechnologyDomain) -> list[str]:
        """Identify risk factors for a technology domain."""
        risks = ["market adoption uncertainty", "regulatory hurdles"]
        if domain.maturity_level == "emerging":
            risks.append("technical feasibility risk")
        if domain.maturity_level == "experimental":
            risks.append("prototype validation risk")
        return risks

    def _market_position(self, market_share: float) -> str:
        """Classify market position based on share."""
        if market_share >= 0.4:
            return "leader"
        if market_share >= 0.2:
            return "challenger"
        if market_share >= 0.05:
            return "niche"
        return "entrant"

    def _threat_level(self, market_share: float) -> TrendImpact:
        """Classify threat level from a competitor's market share."""
        if market_share >= 0.35:
            return TrendImpact.transformative
        if market_share >= 0.15:
            return TrendImpact.high
        return TrendImpact.medium

    def _opportunity_from_weakness(self, competitor: Competitor) -> str:
        """Derive an opportunity string from a competitor's weakness."""
        weakness = competitor.weaknesses[0] if competitor.weaknesses else "unknown weakness"
        return f"Exploit competitor weakness: {weakness}"

    def _scenario_likelihood(self, signal: TrendSignal) -> ScenarioLikelihood:
        """Determine scenario likelihood from signal confidence."""
        if signal.confidence >= 0.85:
            return ScenarioLikelihood.certain
        if signal.confidence >= 0.7:
            return ScenarioLikelihood.likely
        if signal.confidence >= 0.5:
            return ScenarioLikelihood.possible
        return ScenarioLikelihood.unlikely

    def _scenario_implications(self, signal: TrendSignal) -> list[str]:
        """Generate implications for a scenario."""
        return [
            f"Market disruption risk from {signal.name}",
            f"Required strategic pivot in {signal.category.value}",
            f"Resource reallocation needed for {signal.timeframe.value}",
        ]

    def _scenario_actions(self, signal: TrendSignal) -> list[str]:
        """Generate recommended actions for a scenario."""
        return [
            f"Monitor {signal.name} development closely",
            f"Build capabilities in {signal.category.value}",
            f"Engage early adopters of {signal.name}",
        ]


def context_domain_placeholder(signal: TrendSignal) -> str:
    """Return a context label for scenario descriptions."""
    return signal.category.value


__all__ = ["StrategyAnalysisEngine"]
