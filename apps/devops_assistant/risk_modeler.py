"""
DevOps Risk Modeler
===================

Quantitative risk scoring for deployment and infrastructure changes.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.schemas import RiskScore

logger = logging.getLogger(__name__)


class DevOpsRiskModeler:
    """Quantitative risk scoring for DevOps changes."""

    def score(self, context: dict[str, Any]) -> RiskScore:
        probability = self._calculate_probability(context)
        impact = self._calculate_impact(context)
        reversibility = self._calculate_reversibility(context)
        overall = self._calculate_overall(probability, impact, reversibility)
        return RiskScore(
            probability=probability,
            impact=impact,
            reversibility=reversibility,
            overall=overall,
        )

    def _calculate_probability(self, context: dict[str, Any]) -> float:
        score = 0.3
        if context.get("has_tests"):
            score -= 0.1
        if context.get("has_rollback"):
            score -= 0.15
        if context.get("has_health_checks"):
            score -= 0.1
        if context.get("is_canary"):
            score -= 0.1
        return max(0.0, min(1.0, score))

    def _calculate_impact(self, context: dict[str, Any]) -> float:
        score = 0.5
        if context.get("critical_service"):
            score += 0.2
        if context.get("high_traffic"):
            score += 0.1
        if context.get("data_migration"):
            score += 0.2
        if context.get("multi_region"):
            score += 0.1
        return max(0.0, min(1.0, score))

    def _calculate_reversibility(self, context: dict[str, Any]) -> float:
        score = 0.7
        if context.get("has_rollback"):
            score += 0.2
        if context.get("database_changes"):
            score -= 0.3
        if context.get("irreversible"):
            score -= 0.4
        return max(0.0, min(1.0, score))

    def _calculate_overall(self, probability: float, impact: float, reversibility: float) -> float:
        return probability * 0.4 + impact * 0.4 + (1.0 - reversibility) * 0.2
