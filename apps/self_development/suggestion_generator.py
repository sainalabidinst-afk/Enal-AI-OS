"""
Suggestion Generator
====================

Generates prioritized improvement proposals with confidence scores.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.self_development.schemas import Problem, ProblemType, Solution

logger = logging.getLogger(__name__)

IMPROVEMENT_MAP: dict[str, dict[str, Any]] = {
    ProblemType.BOTTLENECK.value: {
        "solution_type": "refactor",
        "estimated_effort": "medium",
        "risk": "medium",
        "tests_required": True,
        "description_template": "Refactor {location} for concurrent or batched processing to reduce latency.",
    },
    ProblemType.DEAD_CODE.value: {
        "solution_type": "refactor",
        "estimated_effort": "low",
        "risk": "low",
        "tests_required": True,
        "description_template": "Remove unused method {location} after confirming no callers.",
    },
    ProblemType.DUPLICATION.value: {
        "solution_type": "refactor",
        "estimated_effort": "medium",
        "risk": "medium",
        "tests_required": True,
        "description_template": "Extract shared logic from {location} into a reusable helper.",
    },
    ProblemType.ARCHITECTURE_SMELL.value: {
        "solution_type": "restructure",
        "estimated_effort": "high",
        "risk": "high",
        "tests_required": True,
        "description_template": "Restructure {location} to reduce coupling and respect module boundaries.",
    },
    ProblemType.SECURITY_HOLE.value: {
        "solution_type": "security_hardening",
        "estimated_effort": "medium",
        "risk": "medium",
        "tests_required": True,
        "description_template": "Harden {location} by removing hardcoded secrets and adopting secret management.",
    },
    ProblemType.PERFORMANCE_ISSUE.value: {
        "solution_type": "optimize",
        "estimated_effort": "medium",
        "risk": "medium",
        "tests_required": True,
        "description_template": "Optimize {location} with caching, indexing, or batching.",
    },
    ProblemType.TEST_COVERAGE_GAP.value: {
        "solution_type": "testing",
        "estimated_effort": "medium",
        "risk": "low",
        "tests_required": True,
        "description_template": "Add regression tests for {location} to close coverage gap.",
    },
    ProblemType.DEPENDENCY_CYCLE.value: {
        "solution_type": "restructure",
        "estimated_effort": "high",
        "risk": "high",
        "tests_required": True,
        "description_template": "Break dependency cycle involving {location} by introducing an abstraction.",
    },
    ProblemType.LAYER_VIOLATION.value: {
        "solution_type": "refactor",
        "estimated_effort": "medium",
        "risk": "medium",
        "tests_required": True,
        "description_template": "Fix layer violation in {location} by restoring the correct dependency direction.",
    },
    ProblemType.API_CONTRACT_BREAKING.value: {
        "solution_type": "refactor",
        "estimated_effort": "high",
        "risk": "high",
        "tests_required": True,
        "description_template": "Restore or version the API contract at {location} to avoid breaking clients.",
    },
}


class SuggestionGenerator:
    """Produces prioritized improvement proposals from detected problems."""

    def propose(self, problem: Problem) -> Solution:
        template = IMPROVEMENT_MAP.get(problem.type, IMPROVEMENT_MAP[ProblemType.BOTTLENECK.value])
        description = template["description_template"].format(location=problem.location)
        confidence = max(0.0, min(1.0, problem.confidence - 0.05))
        return Solution(
            problem_id=problem.id,
            solution_type=template["solution_type"],
            description=description,
            estimated_effort=template["estimated_effort"],
            risk=template["risk"],
            tests_required=template["tests_required"],
            confidence=confidence,
        )
