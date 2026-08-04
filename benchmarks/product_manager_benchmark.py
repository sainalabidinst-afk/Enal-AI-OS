"""
Product Manager Benchmark
=========================

Benchmark scenarios for validating Product Manager capability pack.
Target: A- (≥85%) with 10 scenarios across 6 dimensions.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "pm-001",
        "name": "Product Vision Definition",
        "category": "product_vision",
        "inputs": {
            "business_context": {"project_name": "new-product-vision", "domain": "saas"},
            "inputs": {"market": "SMB", "vision_horizon_years": 3, "target_users": ["startups", "freelancers"]},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-002",
        "name": "Product Roadmap Planning",
        "category": "roadmap",
        "inputs": {
            "business_context": {"project_name": "roadmap-2025", "domain": "saas"},
            "inputs": {"quarters": 4, "themes": ["growth", "retention", "monetization"]},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-003",
        "name": "Backlog Prioritization",
        "category": "backlog",
        "inputs": {
            "business_context": {"project_name": "backlog-priority", "domain": "saas"},
            "inputs": {"items_count": 50, "framework": "RICE"},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-004",
        "name": "Sprint Planning",
        "category": "sprint",
        "inputs": {
            "business_context": {"project_name": "sprint-24", "domain": "saas"},
            "inputs": {"sprint_duration_weeks": 2, "team_capacity_points": 30},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "pm-005",
        "name": "OKR Definition and Tracking",
        "category": "okr",
        "inputs": {
            "business_context": {"project_name": "okr-q1", "domain": "saas"},
            "inputs": {"objectives_count": 3, "krs_per_objective": 3},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-006",
        "name": "KPI Dashboard Design",
        "category": "kpi",
        "inputs": {
            "business_context": {"project_name": "kpi-dashboard", "domain": "enterprise"},
            "inputs": {"metrics": ["MRR", "Churn", "NPS", "CAC"], "target_accuracy": 0.95},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-007",
        "name": "Product Discovery untuk Fitur Baru",
        "category": "discovery",
        "inputs": {
            "business_context": {"project_name": "discovery-auth", "domain": "saas"},
            "inputs": {"user_segments": ["enterprise", "smb"], "research_methods": ["interview", "survey"]},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-008",
        "name": "Release Planning",
        "category": "release",
        "inputs": {
            "business_context": {"project_name": "release-v2", "domain": "saas"},
            "inputs": {"features_count": 8, "rollout_strategy": "canary", "target_date": "2025-06-01"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "pm-009",
        "name": "Feature Prioritization Matrix",
        "category": "prioritization",
        "inputs": {
            "business_context": {"project_name": "priority-matrix", "domain": "saas"},
            "inputs": {"features": 20, "criteria": ["impact", "effort", "risk", "strategic_fit"]},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "pm-010",
        "name": "Stakeholder Alignment Workshop",
        "category": "alignment",
        "inputs": {
            "business_context": {"project_name": "alignment-q2", "domain": "enterprise"},
            "inputs": {"stakeholders": ["engineering", "sales", "support"], "conflicts": ["resource", "timeline"]},
        },
        "min_quality_score": 0.85,
    },
]


def get_scenarios() -> list[dict[str, Any]]:
    return SCENARIOS


def get_scenario_by_id(scenario_id: str) -> dict[str, Any] | None:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None
