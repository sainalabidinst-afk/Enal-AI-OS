"""
System Architect — CQRS Evaluator.

Evaluates Command Query Responsibility Segregation patterns:
- Command/query separation analysis
- Read/write model detection
- CQRS anti-pattern identification (e.g., write-through reads)
- Suitability assessment for the project
- Event sourcing readiness when combined with CQRS
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


class CQRSEvaluator:
    """
    Evaluates a project for CQRS conformance and suitability.

    Usage::
        evaluator = CQRSEvaluator(repo_path)
        findings, recs = await evaluator.analyze()
    """

    COMMAND_HINTS = ("command", "write", "create", "update", "delete", "post", "put", "submit", "execute")
    QUERY_HINTS = ("query", "read", "get", "find", "list", "search", "fetch", "retrieve", "load")
    SEPARATION_HINTS = ("command", "query", "queries", "commands", "cqrs", "write_model", "read_model")
    ANTI_PATTERN_HINTS = ("write_through", "read_through", "same_model", "shared_model")

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)

    async def analyze(self) -> tuple[list[Finding], list[Recommendation]]:
        """Run CQRS evaluation."""
        findings: list[Finding] = []
        commands: list[str] = []
        queries: list[str] = []
        command_models: list[str] = []
        query_models: list[str] = []
        mixed_modules: list[str] = []
        anti_patterns: list[str] = []

        for py_file in self.repo_path.rglob("*.py"):
            module_path = str(py_file.relative_to(self.repo_path))
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except (SyntaxError, Exception):
                continue

            has_command = False
            has_query = False

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    lower = node.name.lower()
                    if self._is_command(lower):
                        commands.append(f"{module_path}:{node.name}")
                        has_command = True
                    elif self._is_query(lower):
                        queries.append(f"{module_path}:{node.name}")
                        has_query = True
                elif isinstance(node, ast.ClassDef):
                    lower = node.name.lower()
                    if any(h in lower for h in self.SEPARATION_HINTS):
                        if "command" in lower or "write" in lower:
                            command_models.append(f"{module_path}:{node.name}")
                        if "query" in lower or "read" in lower:
                            query_models.append(f"{module_path}:{node.name}")
                    lower_path = module_path.lower()
                    if any(h in lower_path for h in self.ANTI_PATTERN_HINTS):
                        anti_patterns.append(f"{module_path}:{node.name}")

            if has_command and has_query:
                mixed_modules.append(module_path)

        # Findings
        findings.extend(self._analyze_separation(commands, queries, mixed_modules))
        findings.extend(self._analyze_models(command_models, query_models))
        findings.extend(self._analyze_anti_patterns(anti_patterns))
        findings.extend(self._analyze_suitability(commands, queries))

        recommendations = self._generate_recommendations(findings)

        return findings, recommendations

    # ------------------------------------------------------------------
    # Analysis methods
    # ------------------------------------------------------------------

    def _is_command(self, name: str) -> bool:
        return any(h in name for h in self.COMMAND_HINTS)

    def _is_query(self, name: str) -> bool:
        return any(h in name for h in self.QUERY_HINTS)

    def _analyze_separation(
        self,
        commands: list[str],
        queries: list[str],
        mixed_modules: list[str],
    ) -> list[Finding]:
        findings: list[Finding] = []
        if not commands and not queries:
            return findings

        if mixed_modules:
            findings.append(
                Finding(
                    category=FindingCategory.cqrs_mismatch,
                    severity=Severity.medium,
                    title=f"{len(mixed_modules)} module(s) mix commands and queries",
                    description=(
                        "The following modules contain both command (write) and query "
                        "(read) operations: " + ", ".join(mixed_modules[:5]) +
                        ". Mixing commands and queries can complicate caching, "
                        "scaling, and transaction management."
                    ),
                    evidence={
                        "mixed_modules": mixed_modules,
                        "command_count": len(commands),
                        "query_count": len(queries),
                    },
                    recommendation=(
                        "If the application has significantly different read and write "
                        "loads, consider splitting command and query paths (CQRS). "
                        "Otherwise, ensure consistent use of repositories."
                    ),
                    impact=Impact.scalability,
                    confidence=0.7,
                )
            )
        else:
            findings.append(
                Finding(
                    category=FindingCategory.cqrs_mismatch,
                    severity=Severity.low,
                    title="Commands and queries are separated",
                    description=(
                        "Command and query operations appear separated, which is a "
                        "good foundation for CQRS if needed."
                    ),
                    evidence={
                        "command_count": len(commands),
                        "query_count": len(queries),
                    },
                    recommendation=(
                        "Maintain separation; introduce read models only if "
                        "query load warrants it."
                    ),
                    impact=Impact.scalability,
                    confidence=0.7,
                )
            )
        return findings

    def _analyze_models(
        self,
        command_models: list[str],
        query_models: list[str],
    ) -> list[Finding]:
        findings: list[Finding] = []
        if command_models and query_models:
            findings.append(
                Finding(
                    category=FindingCategory.cqrs_mismatch,
                    severity=Severity.low,
                    title="Read/write models present",
                    description=(
                        f"Found {len(command_models)} command/write model(s) and "
                        f"{len(query_models)} query/read model(s), consistent with "
                        "CQRS architecture."
                    ),
                    evidence={
                        "command_models": command_models[:5],
                        "query_models": query_models[:5],
                    },
                    recommendation=(
                        "Ensure query models are optimized for read patterns and "
                        "maintain consistency mechanisms with write models."
                    ),
                    impact=Impact.scalability,
                    confidence=0.75,
                )
            )
        return findings

    def _analyze_anti_patterns(self, anti_patterns: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if anti_patterns:
            findings.append(
                Finding(
                    category=FindingCategory.cqrs_mismatch,
                    severity=Severity.high,
                    title="CQRS anti-pattern detected (write-through reads)",
                    description=(
                        "Detected modules that may use the same model for reads and "
                        "writes (write-through reads anti-pattern): "
                        + ", ".join(anti_patterns[:5])
                    ),
                    evidence={"anti_pattern_modules": anti_patterns},
                    recommendation=(
                        "Separate read paths from write paths; consider materialized "
                        "views or projections for read models."
                    ),
                    impact=Impact.scalability,
                    confidence=0.65,
                )
            )
        return findings

    def _analyze_suitability(self, commands: list[str], queries: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if not commands and not queries:
            return findings
        ratio = len(queries) / max(1, len(commands))
        if ratio >= 4.0:
            findings.append(
                Finding(
                    category=FindingCategory.cqrs_mismatch,
                    severity=Severity.low,
                    title="Read-heavy workload detected",
                    description=(
                        f"Query-to-command ratio is {ratio:.1f}:1. "
                        "This read-heavy workload is a strong candidate for CQRS "
                        "with separate read models."
                    ),
                    evidence={
                        "query_count": len(queries),
                        "command_count": len(commands),
                        "ratio": round(ratio, 2),
                    },
                    recommendation=(
                        "Evaluate introducing read-optimized models or query "
                        "projections to reduce load on the write model."
                    ),
                    impact=Impact.scalability,
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
                    problem="CQRS mismatch or anti-pattern detected",
                    solution=(
                        "Separate command and query paths. Use read models/projections "
                        "for queries when read-write ratio is high. "
                        "Document the consistency model."
                    ),
                    effort=Effort.high,
                    impact="Improves scalability and query performance",
                )
            )
        if any(f.category == FindingCategory.cqrs_mismatch and f.severity == Severity.low for f in findings):
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="Potential CQRS improvement opportunity",
                    solution=(
                        "Continuously monitor the read/write ratio. Introduce "
                        "read models when query load becomes asymmetric."
                    ),
                    effort=Effort.medium,
                    impact="Future scalability headroom",
                )
            )
        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No significant CQRS issues",
                    solution="Maintain current command/query separation.",
                    effort=Effort.low,
                    impact="Preserves current design",
                )
            )
        return recs

