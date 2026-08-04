"""
Simulation Engine — outcome prediction for decision alternatives.

Simulates likely outcomes for each alternative based on evidence,
objectives, and historical patterns. Produces expected-value estimates
and confidence intervals that downstream scoring can consume.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from apps.decision_intelligence.schemas import EvidenceSource, Objective, RiskProfile


@dataclass
class SimulationOutcome:
    """Predicted outcome for a single alternative."""

    alternative_description: str
    expected_value: float = 0.0
    confidence_interval: tuple[float, float] = (0.0, 0.0)
    probability_of_success: float = 0.0
    key_drivers: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


class SimulationEngine:
    """
    Estimates outcome distributions for decision alternatives.

    Usage::

        engine = SimulationEngine()
        outcome = engine.simulate(alternative_description, evidence_set, objectives)
    """

    def simulate(
        self,
        description: str,
        evidence_set: Any,
        objectives: list[Objective],
        risk_profile: RiskProfile | None = None,
    ) -> SimulationOutcome:
        """
        Produce a simulated outcome for the given alternative.

        Args:
            description: Alternative description.
            evidence_set: Aggregated evidence.
            objectives: Weighted objectives.
            risk_profile: Optional risk assessment.

        Returns:
            SimulationOutcome with expected value, confidence interval, and drivers.
        """
        base = self._base_score(description, evidence_set)
        objective_boost = self._objective_boost(objectives)
        risk_penalty = (risk_profile.overall_risk if risk_profile else 0.0) * 0.3
        expected_value = max(0.0, min(1.0, base + objective_boost - risk_penalty))

        spread = 0.1 + (risk_profile.overall_risk if risk_profile else 0.0) * 0.2
        lower = max(0.0, expected_value - spread)
        upper = min(1.0, expected_value + spread)

        prob_success = expected_value
        drivers = self._extract_drivers(evidence_set)
        assumptions = self._extract_assumptions(evidence_set, objectives)

        return SimulationOutcome(
            alternative_description=description,
            expected_value=round(expected_value, 4),
            confidence_interval=(round(lower, 4), round(upper, 4)),
            probability_of_success=round(prob_success, 4),
            key_drivers=drivers,
            assumptions=assumptions,
            raw={
                "base_score": round(base, 4),
                "objective_boost": round(objective_boost, 4),
                "risk_penalty": round(risk_penalty, 4),
            },
        )

    def _base_score(self, description: str, evidence_set: Any) -> float:
        if evidence_set is None or not getattr(evidence_set, "items", []):
            return 0.5
        sentiment = getattr(evidence_set, "dominant_sentiment", "neutral")
        avg_quality = getattr(evidence_set, "avg_quality", 0.5)
        if sentiment == "positive":
            return 0.5 + avg_quality * 0.4
        if sentiment == "negative":
            return 0.5 - avg_quality * 0.3
        return 0.5

    def _objective_boost(self, objectives: list[Objective]) -> float:
        if not objectives:
            return 0.0
        return sum(o.weight for o in objectives) / len(objectives) * 0.1

    def _extract_drivers(self, evidence_set: Any) -> list[str]:
        if evidence_set is None or not getattr(evidence_set, "items", []):
            return ["limited evidence"]
        drivers: list[str] = []
        for item in evidence_set.items[:3]:
            payload = item.payload or {}
            for key in ("score", "recommendation", "sentiment", "risk"):
                if key in payload:
                    drivers.append(f"{item.source_id}:{key}={payload[key]}")
                    break
        return drivers or ["general evidence"]

    def _extract_assumptions(self, evidence_set: Any, objectives: list[Objective]) -> list[str]:
        assumptions = [
            "Evidence quality is representative of real-world conditions",
            "Objective weights remain stable over the decision horizon",
        ]
        if objectives:
            assumptions.append(f"Optimizing for: {', '.join(o.name for o in objectives)}")
        return assumptions
