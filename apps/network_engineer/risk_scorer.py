"""
Risk Scoring Engine
====================

Computes risk scores before deployment.
Config Risk, Rollback Risk, Security Risk, Downtime Risk.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class RiskScore:
    config_risk: float = 0.0
    rollback_risk: float = 0.0
    security_risk: float = 0.0
    downtime_risk: float = 0.0
    overall_risk: float = 0.0
    recommendation: str = ""
    factors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_risk": round(self.config_risk, 2),
            "rollback_risk": round(self.rollback_risk, 2),
            "security_risk": round(self.security_risk, 2),
            "downtime_risk": round(self.downtime_risk, 2),
            "overall_risk": round(self.overall_risk, 2),
            "recommendation": self.recommendation,
            "factors": self.factors,
        }


class RiskScoringEngine:
    """Computes risk scores for configuration changes."""

    def score(self, diff_summary: dict[str, int], findings: list[dict[str, Any]], is_new_device: bool = False) -> RiskScore:
        """Compute risk scores from diff summary and analysis findings."""
        config_risk = self._compute_config_risk(diff_summary)
        security_risk = self._compute_security_risk(findings)
        downtime_risk = self._compute_downtime_risk(diff_summary)
        rollback_risk = self._compute_rollback_risk(is_new_device)

        overall = (config_risk * 0.3 + security_risk * 0.3 + downtime_risk * 0.25 + rollback_risk * 0.15)

        factors = []
        if diff_summary.get("removed", 0) > 0:
            factors.append(f"{diff_summary['removed']} rules will be removed")
        if security_risk > 0.3:
            factors.append("Security findings present")
        if downtime_risk > 0.3:
            factors.append("High downtime risk")
        if is_new_device:
            factors.append("No baseline for rollback")

        recommendation = self._generate_recommendation(overall, factors)

        return RiskScore(
            config_risk=config_risk,
            rollback_risk=rollback_risk,
            security_risk=security_risk,
            downtime_risk=downtime_risk,
            overall_risk=overall,
            recommendation=recommendation,
            factors=factors,
        )

    def _compute_config_risk(self, diff_summary: dict[str, int]) -> float:
        total_changes = diff_summary.get("added", 0) + diff_summary.get("removed", 0) + diff_summary.get("modified", 0)
        if total_changes == 0:
            return 0.0
        # More changes = more risk
        risk = min(total_changes / 20.0, 1.0)
        # Removals are riskier than additions
        if diff_summary.get("removed", 0) > 0:
            risk += 0.2
        return min(risk, 1.0)

    def _compute_security_risk(self, findings: list[dict[str, Any]]) -> float:
        if not findings:
            return 0.0
        critical = sum(1 for f in findings if f.get("severity") == "critical")
        warnings = sum(1 for f in findings if f.get("severity") == "warning")
        risk = (critical * 0.3 + warnings * 0.1)
        return min(risk, 1.0)

    def _compute_downtime_risk(self, diff_summary: dict[str, int]) -> float:
        # Changes to firewall, routes, interfaces are riskier
        risk = 0.0
        if diff_summary.get("modified", 0) > 5:
            risk += 0.2
        if diff_summary.get("removed", 0) > 0:
            risk += 0.2
        # Large changes increase downtime risk
        total = diff_summary.get("added", 0) + diff_summary.get("removed", 0) + diff_summary.get("modified", 0)
        if total > 10:
            risk += 0.2
        return min(risk, 1.0)

    def _compute_rollback_risk(self, is_new_device: bool) -> float:
        if is_new_device:
            return 0.3  # No baseline to rollback to
        return 0.05  # Backup available

    def _generate_recommendation(self, overall: float, factors: list[str]) -> str:
        if overall < 0.2:
            return "Low risk. Safe to proceed with approval."
        elif overall < 0.5:
            return "Medium risk. Review changes carefully before approval."
        elif overall < 0.8:
            return "High risk. Strongly recommend manual review and staged rollout."
        else:
            return "Critical risk. Do not deploy without senior engineer approval."


risk_scoring_engine = RiskScoringEngine()
