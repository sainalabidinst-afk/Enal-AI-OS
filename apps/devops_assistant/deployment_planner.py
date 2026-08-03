"""
Deployment Planner
==================

Plans deployment strategies: rolling, blue-green, canary, and feature flags.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.schemas import Problem, Solution

logger = logging.getLogger(__name__)

DEPLOYMENT_STRATEGIES: dict[str, dict[str, Any]] = {
    "rolling": {
        "name": "Rolling Update",
        "risk": "low",
        "downtime": "none",
        "rollback": "automated",
        "use_cases": ["standard deployments", "frequent releases"],
    },
    "blue_green": {
        "name": "Blue/Green",
        "risk": "low",
        "downtime": "none",
        "rollback": "instant",
        "use_cases": ["zero-downtime migrations", "major version changes"],
    },
    "canary": {
        "name": "Canary",
        "risk": "medium",
        "downtime": "none",
        "rollback": "automated",
        "use_cases": ["high-risk changes", "gradual rollout"],
    },
    "feature_flag": {
        "name": "Feature Flag",
        "risk": "low",
        "downtime": "none",
        "rollback": "instant",
        "use_cases": ["A/B testing", "gradual feature rollout"],
    },
}


class DeploymentPlanner:
    """Plans deployment strategies."""

    def plan(self, service_name: str, strategy: str = "rolling") -> dict[str, Any]:
        strategy_config = DEPLOYMENT_STRATEGIES.get(strategy, DEPLOYMENT_STRATEGIES["rolling"])
        return {
            "service": service_name,
            "strategy": strategy,
            "config": strategy_config,
            "steps": [
                "Build container image",
                "Push to registry",
                "Update deployment manifest",
                "Verify rollout health",
                "Promote or rollback",
            ],
            "features": ["automated_rollback", "health_checks", "metrics_validation"],
        }

    def suggest_improvements(self, current_plan: dict[str, Any]) -> list[Solution]:
        solutions: list[Solution] = []
        strategy = current_plan.get("strategy", "rolling")
        features = current_plan.get("features", [])

        if strategy == "rolling" and "automated_rollback" not in features:
            solutions.append(Solution(
                problem_id=f"{current_plan.get('service', 'unknown')}-missing-rollback",
                solution_type=ImprovementType.DEPLOYMENT.value,
                description="Tambahkan automated rollback untuk rolling update strategy.",
                estimated_effort="medium",
                risk="low",
                tests_required=True,
                confidence=0.9,
            ))

        if "metrics_validation" not in features:
            solutions.append(Solution(
                problem_id=f"{current_plan.get('service', 'unknown')}-missing-metrics",
                solution_type=ImprovementType.MONITORING.value,
                description="Tambahkan validasi metrik ke deployment plan.",
                estimated_effort="low",
                risk="low",
                tests_required=True,
                confidence=0.95,
            ))

        return solutions
