"""
UI/UX Designer Benchmark
========================

Benchmark scenarios for validating UI/UX Designer capability pack.
Target: A- (≥85%) with 10 scenarios across 6 dimensions.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "ux-001",
        "name": "E-Commerce User Journey",
        "category": "user_journey",
        "inputs": {
            "business_context": {"project_name": "ecommerce-ux", "domain": "e-commerce"},
            "inputs": {"user_segments": ["buyer", "seller"], "touchpoints": 8},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "ux-002",
        "name": "Design System untuk SaaS Platform",
        "category": "design_system",
        "inputs": {
            "business_context": {"project_name": "saas-design-system", "domain": "saas"},
            "inputs": {"components_count": 30, "tokens": ["color", "typography", "spacing"]},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "ux-003",
        "name": "Mobile Banking Wireframe",
        "category": "wireframe",
        "inputs": {
            "business_context": {"project_name": "mobile-banking", "domain": "fintech"},
            "inputs": {"screens_count": 12, "platform": "mobile"},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "ux-004",
        "name": "Dashboard Analytics Prototype",
        "category": "prototype",
        "inputs": {
            "business_context": {"project_name": "analytics-dashboard", "domain": "enterprise"},
            "inputs": {"fidelity": "high", "interactions": 15, "screens": 6},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "ux-005",
        "name": "WCAG 2.1 AA Accessibility Audit",
        "category": "accessibility",
        "inputs": {
            "business_context": {"project_name": "a11y-audit", "domain": "enterprise"},
            "inputs": {"target_level": "AA", "check_contrast": True, "check_keyboard": True},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "ux-006",
        "name": "Interaction Design untuk Form Complex",
        "category": "interaction",
        "inputs": {
            "business_context": {"project_name": "form-interaction", "domain": "enterprise"},
            "inputs": {"form_fields": 20, "validation_rules": 15, "error_states": True},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "ux-007",
        "name": "UX Research untuk Redesign",
        "category": "ux_research",
        "inputs": {
            "business_context": {"project_name": "redesign-research", "domain": "e-commerce"},
            "inputs": {"user_interviews": 10, "surveys": 100, "personas": 3},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "ux-008",
        "name": "Design Review untuk E-Commerce",
        "category": "design_review",
        "inputs": {
            "business_context": {"project_name": "design-review", "domain": "e-commerce"},
            "inputs": {"screens": 20, "review_criteria": ["consistency", "accessibility", "usability"]},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "ux-009",
        "name": "Responsive Breakpoint Planning",
        "category": "prototype",
        "inputs": {
            "business_context": {"project_name": "responsive-design", "domain": "saas"},
            "inputs": {"breakpoints": ["mobile", "tablet", "desktop"], "components": 50},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "ux-010",
        "name": "Component Props Schema Design",
        "category": "design_system",
        "inputs": {
            "business_context": {"project_name": "props-schema", "domain": "developer-tools"},
            "inputs": {"component_types": ["button", "input", "modal"], "variants_per_component": 4},
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
