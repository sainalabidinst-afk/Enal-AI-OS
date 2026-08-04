"""
Documentation Engineer Benchmark
===================================

Benchmark scenarios for validating Documentation Engineer capability pack.
Target: A (≥90%) with 10 scenarios across 6 dimensions.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "docs-001",
        "name": "OpenAPI Documentation Generation",
        "category": "openapi",
        "inputs": {
            "business_context": {"project_name": "api-docs", "domain": "software-development"},
            "inputs": {"source_type": "fastapi", "output_format": "yaml"},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "docs-002",
        "name": "SDK Documentation Generation",
        "category": "sdk_docs",
        "inputs": {
            "business_context": {"project_name": "sdk-docs", "domain": "developer-tools"},
            "inputs": {"language": "python", "include_examples": True},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "docs-003",
        "name": "Architecture Documentation",
        "category": "architecture",
        "inputs": {
            "business_context": {"project_name": "arch-docs", "domain": "enterprise"},
            "inputs": {"source_type": "adr", "adr_count": 5},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "docs-004",
        "name": "Release Notes Generation",
        "category": "release_notes",
        "inputs": {
            "business_context": {"project_name": "release-notes", "domain": "software-development"},
            "inputs": {"version": "1.2.0", "changes_count": 15},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "docs-005",
        "name": "Documentation Validation",
        "category": "validation",
        "inputs": {
            "business_context": {"project_name": "docs-validation", "domain": "enterprise"},
            "inputs": {"validation_rules": ["broken_links", "missing_sections", "outdated_examples"]},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "docs-006",
        "name": "RFC Documentation Generation",
        "category": "rfc",
        "inputs": {
            "business_context": {"project_name": "rfc-docs", "domain": "software-development"},
            "inputs": {"rfc_type": "feature", "sections": ["motivation", "design", "alternatives"]},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "docs-007",
        "name": "Multi-Language SDK Docs",
        "category": "sdk_docs",
        "inputs": {
            "business_context": {"project_name": "polyglot-sdk", "domain": "developer-tools"},
            "inputs": {"languages": ["python", "typescript", "go"], "include_code_samples": True},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "docs-008",
        "name": "API Changelog Generation",
        "category": "changelog",
        "inputs": {
            "business_context": {"project_name": "api-changelog", "domain": "api-platform"},
            "inputs": {"versions": ["v1", "v2"], "include_breaking_changes": True},
        },
        "min_quality_score": 0.90,
    },
    {
        "id": "docs-009",
        "name": "End-to-End Documentation Sync",
        "category": "sync",
        "inputs": {
            "business_context": {"project_name": "docs-sync", "domain": "enterprise"},
            "inputs": {"packs": ["code_engineer", "devops_assistant", "security_engineer"], "sync_frequency": "daily"},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "docs-010",
        "name": "Documentation Coverage Analysis",
        "category": "validation",
        "inputs": {
            "business_context": {"project_name": "docs-coverage", "domain": "enterprise"},
            "inputs": {"coverage_target": 0.95, "include_undocumented": True},
        },
        "min_quality_score": 0.90,
    },
]


def get_scenarios() -> list[dict[str, Any]]:
    return SCENARIOS


def get_scenario_by_id(scenario_id: str) -> dict[str, Any] | None:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None
