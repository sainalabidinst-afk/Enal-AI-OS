"""
System Architect — Microservices / Monolith Analyzer.

Evaluates service decomposition strategies:
- Monolith-to-microservices migration opportunity
- Service boundary coherence
- Database coupling / shared-schema risks
- Network communication anti-patterns
- Deployment and scalability analysis
- Data ownership analysis
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any

from apps.system_architect.schemas import (
    Finding,
    FindingCategory,
    Severity,
    Impact,
    Recommendation,
    Priority,
    Effort,
)

logger = logging.getLogger(__name__)


class MicroservicesAnalyzer:
    """
    Analyzes a project for microservices/monolith decomposition.

    Usage::
        analyzer = MicroservicesAnalyzer(repo_path)
        findings, recs = await analyzer.analyze()
    """

    SERVICE_HINTS = ("service", "microservice", "svc", "domain_service", "module", "bounded_context")
    SHARED_DB_HINTS = ("shared_db", "shared_database", "global_schema", "single_db")
    ORCHESTRATOR_HINTS = ("monolith", "god_module", "god_class", "god_object", "big_bang")
    API_HINTS = ("grpc", "proto", "rest", "api", "endpoint", "rpc")

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)

    async def analyze(self) -> tuple[list[Finding], list[Recommendation]]:
        """Run microservices/monolith decomposition analysis."""
        findings: list[Finding] = []
        services: list[str] = []
        shared_db: list[str] = []
        orchestrators: list[str] = []
        api_defs: list[str] = []
        all_files: list[str] = []

        for py_file in self.repo_path.rglob("*.py"):
            module_path = str(py_file.relative_to(self.repo_path))
            all_files.append(module_path)
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except (SyntaxError, Exception):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    lower = node.name.lower()
                    if any(h in lower for h in self.SERVICE_HINTS):
                        services.append(f"{module_path}:{node.name}")
                    if any(h in lower for h in self.ORCHESTRATOR_HINTS):
                        orchestrators.append(f"{module_path}:{node.name}")

            lower_path = module_path.lower()
            if any(h in lower_path for h in self.SHARED_DB_HINTS):
                shared_db.append(module_path)
            if any(h in lower_path for h in self.API_HINTS):
                api_defs.append(module_path)

        # Findings
        findings.extend(self._analyze_decomposition(all_files, services))
        findings.extend(self._analyze_database_coupling(shared_db))
        findings.extend(self._analyze_god_modules(orchestrators))
        findings.extend(self._analyze_api_contracts(api_defs, services))

        recommendations = self._generate_recommendations(findings)

        return findings, recommendations

    # ------------------------------------------------------------------
    # Analysis methods
    # ------------------------------------------------------------------

    def _analyze_decomposition(self, all_files: list[str], services: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if not services:
            return findings

        # Heuristic: if a single directory holds many files with deep coupling,
        # it may be a monolith candidate for decomposition.
        if len(services) >= 3:
            findings.append(
                Finding(
                    category=FindingCategory.monolith_anti_pattern,
                    severity=Severity.low,
                    title="Multiple potential services detected",
                    description=(
                        f"Found {len(services)} service-like components. "
                        "Evaluate whether these are genuine independently-deployable "
                        "services or modules within a monolith."
                    ),
                    evidence={
                        "service_count": len(services),
                        "services": services[:10],
                    },
                    recommendation=(
                        "Assess coupling, data ownership, and independent deployability "
                        "before splitting into microservices. Prefer modular monolith "
                        "for small teams."
                    ),
                    impact=Impact.deployability,
                    confidence=0.65,
                )
            )
        return findings

    def _analyze_database_coupling(self, shared_db: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if shared_db:
            findings.append(
                Finding(
                    category=FindingCategory.monolith_anti_pattern,
                    severity=Severity.high,
                    title="Shared database detected",
                    description=(
                        "Modules referencing a shared database schema were found: "
                        + ", ".join(shared_db[:5]) +
                        ". Shared database access couples services, limiting "
                        "independent deployment and scalability."
                    ),
                    evidence={"shared_db_modules": shared_db},
                    recommendation=(
                        "Introduce per-service data ownership or use database "
                        "schema-per-service with contract-based integration."
                    ),
                    impact=Impact.scalability,
                    confidence=0.7,
                )
            )
        return findings

    def _analyze_god_modules(self, orchestrators: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if orchestrators:
            findings.append(
                Finding(
                    category=FindingCategory.monolith_anti_pattern,
                    severity=Severity.medium,
                    title="God module / orchestrator detected",
                    description=(
                        "Modules that may be God modules (single class/directing all logic): "
                        + ", ".join(orchestrators[:5]) +
                        ". These become bottlenecks and are hard to test."
                    ),
                    evidence={"orchestrator_modules": orchestrators},
                    recommendation=(
                        "Decompose God modules by responsibility. Extract use-case "
                        "services and keep orchestration thin."
                    ),
                    impact=Impact.maintainability,
                    confidence=0.7,
                )
            )
        return findings

    def _analyze_api_contracts(self, api_defs: list[str], services: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if services and not api_defs:
            findings.append(
                Finding(
                    category=FindingCategory.monolith_anti_pattern,
                    severity=Severity.medium,
                    title="Services without explicit API contracts",
                    description=(
                        f"Found {len(services)} service-like components but no explicit "
                        "API/interface definitions. For service decomposition, explicit "
                        "API contracts are essential."
                    ),
                    evidence={
                        "services_count": len(services),
                        "api_definitions": len(api_defs),
                    },
                    recommendation=(
                        "Define explicit API contracts (OpenAPI, protobuf, or interface "
                        "abstractions) for each service boundary."
                    ),
                    impact=Impact.deployability,
                    confidence=0.7,
                )
            )
        return findings

    def _generate_recommendations(self, findings: list[Finding]) -> list[Recommendation]:
        recs: list[Recommendation] = []
        if any(f.severity in (Severity.high, Severity.critical) for f in findings):
            recs.append(
                Recommendation(
                    priority=Priority.high,
                    problem="Microservices/monolith issues detected",
                    solution=(
                        "Establish clear service boundaries with explicit API contracts. "
                        "Move toward per-service data ownership. Avoid shared databases."
                    ),
                    effort=Effort.high,
                    impact="Improves scalability and independent deployability",
                )
            )
        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No significant microservices/monolith issues",
                    solution="Maintain current service boundaries; review as scale grows.",
                    effort=Effort.low,
                    impact="Preserves architecture coherence",
                )
            )
        return recs

