"""
DevOps Suggestion Generator
============================

Generates improvement suggestions for infrastructure and pipeline artifacts.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.schemas import Problem, Solution
from apps.devops_assistant.smell_taxonomy import DevOpsSmellTaxonomy
from apps.devops_assistant.risk_modeler import DevOpsRiskModeler

logger = logging.getLogger(__name__)


class DevOpsSuggestionGenerator:
    """Generates improvement suggestions for DevOps artifacts."""

    def __init__(self) -> None:
        self.taxonomy = DevOpsSmellTaxonomy()
        self.risk_modeler = DevOpsRiskModeler()

    def analyze(self, artifact: dict[str, Any]) -> dict[str, Any]:
        problems = self.taxonomy.analyze(artifact)
        suggestions = self._generate_suggestions(artifact, problems)
        risk_score = self.risk_modeler.score(artifact)

        return {
            "artifact": artifact.get("path", "unknown"),
            "problems_count": len(problems),
            "problems": [self._problem_to_dict(p) for p in problems],
            "suggestions": suggestions,
            "risk_score": {
                "probability": risk_score.probability,
                "impact": risk_score.impact,
                "reversibility": risk_score.reversibility,
                "overall": risk_score.overall,
            },
            "summary": self._generate_summary(problems, suggestions, risk_score),
        }

    def _generate_suggestions(
        self, artifact: dict[str, Any], problems: list[Problem]
    ) -> list[dict[str, Any]]:
        suggestions: list[dict[str, Any]] = []
        for problem in problems:
            suggestion = self._suggest_for_problem(problem, artifact)
            suggestions.append(suggestion)
        return suggestions

    def _suggest_for_problem(self, problem: Problem, artifact: dict[str, Any]) -> dict[str, Any]:
        type_solutions: dict[str, dict[str, Any]] = {
            "hardcoded_secret": {
                "solution_type": "security_hardening",
                "description": "Gunakan secret management seperti HashiCorp Vault atau Kubernetes Secrets.",
                "estimated_effort": "medium",
                "risk": "low",
                "confidence": 0.95,
            },
            "missing_health_check": {
                "solution_type": "infrastructure",
                "description": "Tambahkan liveness dan readiness probe ke deployment.",
                "estimated_effort": "low",
                "risk": "low",
                "confidence": 0.9,
            },
            "missing_resource_limit": {
                "solution_type": "infrastructure",
                "description": "Tambahkan resource requests dan limits ke pod spec.",
                "estimated_effort": "low",
                "risk": "low",
                "confidence": 0.95,
            },
            "missing_rollback": {
                "solution_type": "deployment",
                "description": "Konfigurasikan rollback strategy dan revision history limit.",
                "estimated_effort": "medium",
                "risk": "low",
                "confidence": 0.85,
            },
            "outdated_image": {
                "solution_type": "infrastructure",
                "description": "Update ke image tag yang lebih baru dan aman.",
                "estimated_effort": "low",
                "risk": "low",
                "confidence": 0.8,
            },
            "insecure_config": {
                "solution_type": "security_hardening",
                "description": "Hapus privileged mode dan run sebagai non-root user.",
                "estimated_effort": "medium",
                "risk": "medium",
                "confidence": 0.9,
            },
            "missing_monitoring": {
                "solution_type": "monitoring",
                "description": "Tambahkan stack monitoring (Prometheus, Grafana, OpenTelemetry).",
                "estimated_effort": "medium",
                "risk": "low",
                "confidence": 0.85,
            },
            "pipeline_break": {
                "solution_type": "pipeline_fix",
                "description": "Perbaiki pipeline trigger dan konfigurasi CI/CD.",
                "estimated_effort": "medium",
                "risk": "low",
                "confidence": 0.8,
            },
            "missing_backup": {
                "solution_type": "infrastructure",
                "description": "Implementasikan backup strategy untuk data penting.",
                "estimated_effort": "high",
                "risk": "low",
                "confidence": 0.75,
            },
            "policy_violation": {
                "solution_type": "policy_as_code",
                "description": "Implementasikan OPA/Gatekeeper untuk policy enforcement.",
                "estimated_effort": "high",
                "risk": "medium",
                "confidence": 0.7,
            },
        }
        solution = type_solutions.get(
            problem.type,
            {
                "solution_type": "infrastructure",
                "description": "Tinjau dan perbaiki konfigurasi secara manual.",
                "estimated_effort": "medium",
                "risk": "medium",
                "confidence": 0.5,
            },
        )
        return {
            "problem_id": problem.id,
            "problem_type": problem.type,
            "severity": problem.severity,
            **solution,
        }

    def _problem_to_dict(self, problem: Problem) -> dict[str, Any]:
        return {
            "id": problem.id,
            "type": problem.type,
            "severity": problem.severity,
            "location": problem.location,
            "description": problem.description,
            "impact": problem.impact,
            "confidence": problem.confidence,
            "evidence": problem.evidence,
        }

    def _generate_summary(
        self, problems: list[Problem], suggestions: list[dict[str, Any]], risk_score: RiskScore
    ) -> str:
        if not problems:
            return "Tidak ada masalah ditemukan. Konfigurasi DevOps sudah baik."
        critical = sum(1 for p in problems if p.severity == "critical")
        high = sum(1 for p in problems if p.severity == "high")
        parts = [f"{len(problems)} masalah ditemukan."]
        if critical:
            parts.append(f"{critical} kritis.")
        if high:
            parts.append(f"{high} tinggi.")
        parts.append(f"Risk score: {risk_score.overall:.2f}.")
        return " ".join(parts)
