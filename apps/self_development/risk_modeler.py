"""
Risk Modeler
============

Quantitative risk scoring for proposed changes.

Formula:
    overall = probability * 0.4 + impact * 0.4 + (1 - reversibility) * 0.2

The score is normalized to 0.0 - 1.0.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.self_development.schemas import Problem, Solution

logger = logging.getLogger(__name__)

SEVERITY_WEIGHTS: dict[str, float] = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.8,
    "critical": 1.0,
}

EFFORT_WEIGHTS: dict[str, float] = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.8,
}

IMPROVEMENT_TYPE_WEIGHTS: dict[str, float] = {
    "refactor": 0.3,
    "restructure": 0.6,
    "optimize": 0.4,
    "security_hardening": 0.5,
    "testing": 0.2,
    "documentation": 0.1,
}


class RiskModeler:
    """Models change risk from problem + solution signals."""

    def score(self, problem: Problem, solution: Solution | None = None) -> float:
        severity = SEVERITY_WEIGHTS.get(problem.severity.lower(), 0.5)
        probability = min(1.0, severity + (1.0 - problem.confidence) * 0.2)
        impact = severity
        reversibility = 0.7
        if solution:
            reversibility = max(0.1, 1.0 - EFFORT_WEIGHTS.get(solution.estimated_effort.lower(), 0.5))
        overall = probability * 0.4 + impact * 0.4 + (1.0 - reversibility) * 0.2
        return max(0.0, min(1.0, overall))

    def score_from_dicts(self, problem: dict[str, Any], solution: dict[str, Any] | None = None) -> float:
        p = Problem(
            id=problem.get("id", ""),
            type=problem.get("type", ""),
            severity=problem.get("severity", "medium"),
            location=problem.get("location", ""),
            description=problem.get("description", ""),
            impact=problem.get("impact", ""),
            confidence=float(problem.get("confidence", 1.0)),
            evidence=problem.get("evidence", []),
        )
        s = None
        if solution:
            s = Solution(
                problem_id=solution.get("problem_id", p.id),
                solution_type=solution.get("solution_type", "refactor"),
                description=solution.get("description", ""),
                estimated_effort=solution.get("estimated_effort", "medium"),
                risk=solution.get("risk", "medium"),
                tests_required=solution.get("tests_required", True),
                confidence=float(solution.get("confidence", 1.0)),
            )
        return self.score(p, s)
