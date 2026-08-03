"""
Pipeline Generator
==================

Generates CI/CD pipeline configurations for various platforms:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.schemas import Problem, Solution

logger = logging.getLogger(__name__)

PIPELINE_TEMPLATES: dict[str, dict[str, Any]] = {
    "github_actions": {
        "platform": "GitHub Actions",
        "file": ".github/workflows/ci.yml",
        "steps": [
            {"name": "Checkout", "uses": "actions/checkout@v4"},
            {"name": "Setup Python", "uses": "actions/setup-python@v5", "with": {"python-version": "3.11"}},
            {"name": "Install", "run": "pip install -e .[dev]"},
            {"name": "Lint", "run": "ruff check ."},
            {"name": "Type Check", "run": "mypy ."},
            {"name": "Test", "run": "pytest tests/ -v"},
            {"name": "Build", "run": "docker build -t ${{ github.repository }}:${{ github.sha }} ."},
            {"name": "Security Scan", "uses": "trivy-action/trivy-scan@master"},
        ],
    },
    "gitlab_ci": {
        "platform": "GitLab CI",
        "file": ".gitlab-ci.yml",
        "steps": [
            {"stage": "lint", "script": ["ruff check .", "mypy ."]},
            {"stage": "test", "script": ["pytest tests/ -v"]},
            {"stage": "build", "script": ["docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA ."]},
            {"stage": "security", "script": ["trivy image $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"]},
            {"stage": "deploy", "script": ["kubectl apply -f k8s/"], "when": "manual"},
        ],
    },
    "jenkins": {
        "platform": "Jenkins",
        "file": "Jenkinsfile",
        "steps": [
            {"stage": "Checkout", "agent": "any", "steps": ["git checkout main"]},
            {"stage": "Build", "agent": "docker", "steps": ["docker build -t app ."]},
            {"stage": "Test", "agent": "python", "steps": ["pytest tests/ -v"]},
            {"stage": "Deploy", "agent": "k8s", "steps": ["kubectl apply -f k8s/"]},
        ],
    },
}


class PipelineGenerator:
    """Generates CI/CD pipeline configurations."""

    def generate(self, service_name: str, platform: str = "github_actions") -> dict[str, Any]:
        template = PIPELINE_TEMPLATES.get(platform, PIPELINE_TEMPLATES["github_actions"])
        return {
            "service": service_name,
            "platform": template["platform"],
            "file": template["file"],
            "pipeline": template["steps"],
            "features": [
                "automated_testing",
                "security_scanning",
                "container_build",
                "artifact_retention",
                "branch_protection",
            ],
        }

    def suggest_improvements(self, current_pipeline: dict[str, Any]) -> list[Solution]:
        solutions: list[Solution] = []
        steps = current_pipeline.get("pipeline", [])
        step_names = [s.get("name", s.get("stage", "")).lower() for s in steps]

        if not any("security" in name for name in step_names):
            solutions.append(Solution(
                problem_id=f"{current_pipeline.get('service', 'unknown')}-security-scan",
                solution_type=ImprovementType.SECURITY_HARDENING.value,
                description="Tambahkan pemindaian keamanan ke pipeline CI/CD.",
                estimated_effort="medium",
                risk="low",
                tests_required=True,
                confidence=0.9,
            ))

        if not any("rollback" in name or "deploy" in name for name in step_names):
            solutions.append(Solution(
                problem_id=f"{current_pipeline.get('service', 'unknown')}-rollback",
                solution_type=ImprovementType.DEPLOYMENT.value,
                description="Tambahkan strategi rollback otomatis ke pipeline deployment.",
                estimated_effort="medium",
                risk="medium",
                tests_required=True,
                confidence=0.85,
            ))

        return solutions
