"""
Risk Analysis — quantify probability and impact of each alternative.

Provides a standardized risk scoring methodology: probability × impact
per alternative, with configurable risk tolerance and multi-factor
categorisation.
"""

from __future__ import annotations

from typing import Any

from apps.decision_intelligence.schemas import RiskProfile, RiskTolerance


# Risk factor definitions: keyword -> (probability_boost, impact_boost, label)
_RISK_FACTORS: dict[str, tuple[float, float, str]] = {
    "rewrite": (0.4, 0.6, "High code change volume — elevated regression risk"),
    "refactor": (0.2, 0.3, "Moderate code change — risk of unintended side effects"),
    "rollback": (0.3, 0.5, "Rollback complexity — potential extended downtime"),
    "unsupported": (0.5, 0.7, "Unsupported feature or vendor — compatibility risk"),
    "critical": (0.3, 0.8, "Critical path change — high impact if failure occurs"),
    "security": (0.2, 0.7, "Security-sensitive change — must pass additional review"),
    "migration": (0.3, 0.6, "Data or configuration migration — potential data loss"),
    "new_system": (0.4, 0.5, "New system integration — unknown failure modes"),
    "downtime": (0.5, 0.8, "Planned or unplanned downtime — business impact"),
    "vendor": (0.3, 0.4, "Vendor dependency — external factors beyond control"),
    "compliance": (0.2, 0.6, "Regulatory or compliance boundary — audit risk"),
    "experimental": (0.5, 0.4, "Experimental approach — no proven track record"),
    "performance": (0.3, 0.5, "Performance-sensitive change — potential regression"),
    "data_loss": (0.4, 0.9, "Potential data loss — irreversible impact"),
    "large_scope": (0.3, 0.5, "Large scope change — high coordination cost"),
}


class RiskAnalyzer:
    """
    Quantifies risk for decision alternatives.

    Usage::

        analyzer = RiskAnalyzer()
        profile = analyzer.analyze(alternative_description, risk_tolerance, evidence_set)
    """

    def analyze(
        self,
        description: str,
        risk_tolerance: RiskTolerance = RiskTolerance.medium,
        evidence_set: Any = None,
    ) -> RiskProfile:
        """
        Produce a risk profile for a single alternative description.

        Args:
            description: Human-readable description of the alternative.
            risk_tolerance: Low / Medium / High tolerance.
            evidence_set: Optional EvidenceSet for evidence-informed risk.

        Returns:
            RiskProfile with probability, impact, overall_risk, and factors.
        """
        lowered = description.lower()

        # Detect risk factors from the description.
        factors: list[str] = []
        prob = 0.2  # baseline probability
        impact = 0.3  # baseline impact

        for keyword, (p_boost, i_boost, label) in _RISK_FACTORS.items():
            if keyword in lowered:
                factors.append(label)
                prob += p_boost
                impact = max(impact, i_boost)

        # Evidence-informed risk adjustment.
        if evidence_set is not None:
            if evidence_set.avg_quality < 0.4:
                prob += 0.1
                factors.append("Low evidence quality — increased uncertainty")
            if evidence_set.negative_weight > evidence_set.positive_weight:
                prob += 0.1
                impact += 0.1
                factors.append("Negative evidence sentiment — elevated risk")

        # Risk tolerance adjustment.
        if risk_tolerance == RiskTolerance.low:
            impact = min(1.0, impact + 0.1)
            prob = min(1.0, prob + 0.05)
        elif risk_tolerance == RiskTolerance.high:
            impact = max(0.1, impact - 0.1)
            prob = max(0.1, prob - 0.05)

        prob = max(0.0, min(1.0, prob))
        impact = max(0.0, min(1.0, impact))
        overall = round(prob * impact, 4)

        return RiskProfile(
            overall_risk=overall,
            probability=round(prob, 4),
            impact=round(impact, 4),
            risk_factors=factors[:5],  # keep top 5
        )
