"""
Trade-off Analysis — multi-objective, weighted scoring.

Scores alternatives against multiple weighted objectives (accuracy vs.
cost vs. latency, etc.), identifies Pareto-optimal candidates, and
produces a composite trade-off score per alternative.
"""

from __future__ import annotations

from typing import Any

from apps.decision_intelligence.schemas import Objective, ObjectiveGoal, TradeOff


class TradeoffAnalyzer:
    """
    Analyzes multi-objective trade-offs between alternatives.

    Usage::

        analyzer = TradeoffAnalyzer()
        for each alternative:
            tradeoffs = analyzer.score_alternative(alt_desc, objectives, evidence_set)
    """

    # Default dimension values generated from description heuristics.
    def score_alternative(
        self,
        description: str,
        objectives: list[Objective],
        evidence_set: Any = None,
    ) -> TradeOff:
        """
        Produce a TradeOff object with normalized per-dimension scores.

        Heuristic approach: each objective dimension derives a 0-1 score
        from description keywords and evidence alignment.

        Args:
            description: Alternative description.
            objectives: Weighted objectives from the DecisionRequest.
            evidence_set: Optional evidence for alignment scoring.

        Returns:
            TradeOff with dimension scores (0-1).
        """
        lowered = description.lower()
        evidence_quality = evidence_set.avg_quality if evidence_set is not None else 0.5
        dominance = "positive" if (evidence_set is not None and evidence_set.positive_weight > evidence_set.negative_weight) else ("negative" if evidence_set is not None else "neutral")

        # Per-dimension heuristics.
        accuracy = 0.5
        cost = 0.5
        latency = 0.5
        risk = 0.5

        # Accuracy modifiers.
        if any(w in lowered for w in ("rewrite", "new architecture", "full")):
            accuracy += 0.15  # fresh implementation often improves correctness
        if any(w in lowered for w in ("incremental", "staged", "subset", "pilot", "partial")):
            accuracy -= 0.05
        if any(w in lowered for w in ("monitoring", "verification", "test")):
            accuracy += 0.1

        # Cost modifiers.
        if any(w in lowered for w in ("rewrite", "full", "overhaul", "migration")):
            cost += 0.25  # higher implementation cost
        if any(w in lowered for w in ("incremental", "subset", "pilot", "small", "partial")):
            cost -= 0.15  # cheaper
        if any(w in lowered for w in ("monitoring", "verification")):
            cost += 0.05

        # Latency modifiers (time-to-implement for simplicity).
        if any(w in lowered for w in ("full", "rewrite", "overhaul", "migration")):
            latency += 0.2
        if any(w in lowered for w in ("incremental", "subset", "pilot", "small", "partial", "immediately")):
            latency -= 0.15

        # Risk dimension (lower is better).
        if any(w in lowered for w in ("rewrite", "migration", "downtime", "new_system")):
            risk += 0.2
        if any(w in lowered for w in ("incremental", "staged", "pilot", "subset", "rollback", "monitoring")):
            risk -= 0.15

        # Evidence alignment boosts the dominant objective.
        if evidence_set is not None:
            if dominance == "positive":
                accuracy = min(1.0, accuracy + 0.15)
                risk = max(0.0, risk - 0.1)
            elif dominance == "negative":
                risk = min(1.0, risk + 0.1)
                accuracy = max(0.0, accuracy - 0.1)

        # Clamp to 0-1.
        accuracy = max(0.0, min(1.0, round(accuracy, 4)))
        cost = max(0.0, min(1.0, round(cost, 4)))
        latency = max(0.0, min(1.0, round(latency, 4)))
        risk = max(0.0, min(1.0, round(risk, 4)))

        tradeoff = TradeOff(accuracy=accuracy, cost=cost, latency=latency)
        # Store risk as an extra dimension if objectives reference it.
        if any(o.name.lower() in ("risk", "safety", "reliability") for o in objectives):
            tradeoff.risk = risk if hasattr(tradeoff, "risk") else risk  # type: ignore[attr-defined]

        return tradeoff

    def compute_composite_score(
        self,
        description: str,
        objectives: list[Objective],
        evidence_set: Any = None,
    ) -> float:
        """
        Compute a weighted composite score for an alternative.

        Each objective maps to a dimension value, normalized by goal
        direction (maximize/minimize), then multiplied by its weight.

        Returns:
            Composite score in [0, 1].
        """
        tradeoff = self.score_alternative(description, objectives, evidence_set)

        # Build a value lookup; extra dimensions are retained.
        value_map: dict[str, float] = {
            "accuracy": tradeoff.accuracy,
            "cost": tradeoff.cost,
            "latency": tradeoff.latency,
            "risk": getattr(tradeoff, "risk", 0.5),
        }

        if not objectives:
            # Default: equally-weighted across accuracy, risk, cost, latency.
            return round(
                0.35 * value_map["accuracy"]
                + 0.25 * (1 - value_map["risk"])
                + 0.20 * (1 - value_map["cost"])
                + 0.20 * (1 - value_map["latency"]),
                4,
            )

        total_score = 0.0
        weight_sum = sum(o.weight for o in objectives) or 1.0
        for obj in objectives:
            name = obj.name.lower()
            raw = value_map.get(name, 0.5)  # default neutral for unknown dimension
            if obj.goal == ObjectiveGoal.minimize:
                # Lower is better.
                score = 1 - raw
            else:
                score = raw
            total_score += obj.weight * score / weight_sum

        return max(0.0, min(1.0, round(total_score, 4)))

    def identify_pareto_optimal(
        self, alternatives: list[tuple[str, TradeOff]]
    ) -> list[int]:
        """
        Identify Pareto-optimal indices among alternatives.

        An alternative is Pareto-optimal if no other alternative is
        strictly better on all dimensions (accuracy, cost, latency, risk).
        Lower cost/latency/risk is better; higher accuracy is better.

        Args:
            alternatives: List of (description, TradeOff) pairs.

        Returns:
            Indices of Pareto-optimal alternatives.
        """
        pareto: list[int] = []
        for i, (_, theo) in enumerate(alternatives):
            dominated = False
            for j, (_, other) in enumerate(alternatives):
                if i == j:
                    continue
                # Check if other dominates i.
                if (
                    other.accuracy >= theo.accuracy
                    and other.cost <= theo.cost
                    and other.latency <= theo.latency
                    and getattr(other, "risk", 0.5) <= getattr(theo, "risk", 0.5)
                    and (
                        other.accuracy > theo.accuracy
                        or other.cost < theo.cost
                        or other.latency < theo.latency
                        or getattr(other, "risk", 0.5) < getattr(theo, "risk", 0.5)
                    )
                ):
                    dominated = True
                    break
            if not dominated:
                pareto.append(i)
        return pareto
