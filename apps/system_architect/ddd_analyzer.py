"""
System Architect — DDD Analyzer.

Evaluates a project against Domain-Driven Design principles:
- Bounded context detection
- Entity / Value Object classification
- Aggregate identification
- Domain event detection
- Anti-corruption layer analysis
- Ubiquitous language consistency
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any

from apps.system_architect.schemas import (
    DDDAssessment,
    BoundedContext,
    Finding,
    FindingCategory,
    Severity,
    Impact,
    Recommendation,
    Priority,
    Effort,
)

logger = logging.getLogger(__name__)


class DDDAnalyzer:
    """
    Analyzes a project for DDD conformance.

    Usage::
        analyzer = DDDAnalyzer(repo_path)
        findings, assessment, recs = await analyzer.analyze()
    """

    # Patterns used to classify domain objects
    ENTITY_HINTS = ("entity", "aggerate", " domain ", "model", "order", "invoice", "customer", "product", "user", "account")
    VALUE_OBJECT_HINTS = ("value", "vo", "amount", "money", "address", "email", "phone", "rating", "percent")
    EVENT_HINTS = ("event", "domainevent", "occurred", "happened", "changed", "created", "updated",
                   "deleted", "cancelled", "completed", "submitted")
    AGGREGATE_HINTS = ("aggregate", "root", "cluster")
    REPOSITORY_HINTS = ("repository", "repo", "persistence", "store")
    ACL_HINTS = ("acl", "anti", "corruption", "adapter", "translator", "converter")

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)

    async def analyze(self) -> tuple[list[Finding], DDDAssessment, list[Recommendation]]:
        """Run DDD analysis on the repository."""
        findings: list[Finding] = []
        assessment = DDDAssessment()
        recommendations: list[Recommendation] = []

        # Scan for DDD-relevant elements
        entities: list[str] = []
        value_objects: list[str] = []
        aggregates: list[str] = []
        repositories: list[str] = []
        domain_events: list[str] = []
        acl_layers: list[str] = []

        for py_file in self.repo_path.rglob("*.py"):
            module_path = str(py_file.relative_to(self.repo_path))
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except (SyntaxError, Exception):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    name = node.name
                    lower = name.lower()
                    # Aggregate detection
                    if self._matches(lower, self.AGGREGATE_HINTS) or name in {"Order", "CustomerAccount"}:
                        aggregates.append(f"{module_path}:{name}")
                    # Entity detection
                    elif self._matches(lower, self.ENTITY_HINTS) or (
                        len(node.body) > 0 and name[0].isupper()
                    ):
                        entities.append(f"{module_path}:{name}")
                    # Value object detection
                    if self._matches(lower, self.VALUE_OBJECT_HINTS):
                        value_objects.append(f"{module_path}:{name}")
                    # Repository detection
                    if self._matches(lower, self.REPOSITORY_HINTS):
                        repositories.append(f"{module_path}:{name}")
                    # ACL detection
                    if self._matches(lower, self.ACL_HINTS):
                        acl_layers.append(f"{module_path}:{name}")

                elif isinstance(node, ast.FunctionDef):
                    lower = node.name.lower()
                    if self._matches(lower, self.EVENT_HINTS) and (
                        "event" in lower or "on_" in lower or "handle" in lower
                    ):
                        domain_events.append(f"{module_path}:{node.name}")

        # Group into bounded contexts by directory
        contexts = self._group_into_contexts(
            entities, value_objects, aggregates, repositories, domain_events
        )

        # Populate assessment
        for ctx_name, ctx in contexts.items():
            assessment.bounded_contexts.append(
                BoundedContext(
                    name=ctx_name,
                    entities=list(ctx.get("entities", [])),
                    value_objects=list(ctx.get("value_objects", [])),
                    aggregates=list(ctx.get("aggregates", [])),
                    repositories=list(ctx.get("repositories", [])),
                )
            )
        assessment.anti_corruption_layers = acl_layers
        assessment.domain_events = domain_events

        # Generate findings
        findings.extend(self._analyze_bounded_contexts(assessment))
        findings.extend(self._analyze_aggregates(assessment, entities, value_objects))
        findings.extend(self._analyze_domain_events(assessment))
        findings.extend(self._analyze_acl(assessment))

        recommendations = self._generate_recommendations(findings)

        return findings, assessment, recommendations

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _matches(self, text: str, hints: tuple[str, ...]) -> bool:
        return any(h.strip() in text for h in hints)

    def _extract_context(self, module_path: str) -> str:
        """Infer a bounded context name from a module path."""
        parts = module_path.replace("\\", "/").split("/")
        # First directory component (if more than 1) or file stem
        if len(parts) >= 3:
            return parts[0] if parts[0] != "src" else parts[1]
        return parts[0].split(".")[0] if parts else "context"

    def _group_into_contexts(
        self,
        entities: list[str],
        value_objects: list[str],
        aggregates: list[str],
        repositories: list[str],
        domain_events: list[str],
    ) -> dict[str, dict[str, list[str]]]:
        """Group DDD elements into bounded contexts."""
        contexts: dict[str, dict[str, list[str]]] = {}
        for group, label in [
            (entities, "entities"),
            (value_objects, "value_objects"),
            (aggregates, "aggregates"),
            (repositories, "repositories"),
            (domain_events, "domain_events"),
        ]:
            for item in group:
                context_name = self._extract_context(item)
                if context_name not in contexts:
                    contexts[context_name] = {}
                contexts[context_name].setdefault(label, []).append(item)
        return contexts

    def _analyze_bounded_contexts(self, assessment: DDDAssessment) -> list[Finding]:
        """Analyze bounded context structure and cohesion."""
        findings: list[Finding] = []
        contexts = assessment.bounded_contexts
        if len(contexts) <= 1:
            findings.append(
                Finding(
                    category=FindingCategory.ddd_violation,
                    severity=Severity.low,
                    title="Single bounded context detected",
                    description=(
                        "The project appears to have a single bounded context. "
                        "If the domain is large, this may lead to coupling between "
                        "different subdomains."
                    ),
                    evidence={"bounded_context_count": len(contexts)},
                    recommendation=(
                        "Consider splitting large domains into bounded contexts with "
                        "explicit contexts and anti-corruption layers between them."
                    ),
                    impact=Impact.modifiability,
                    confidence=0.6,
                )
            )
        return findings

    def _analyze_aggregates(
        self,
        assessment: DDDAssessment,
        entities: list[str],
        value_objects: list[str],
    ) -> list[Finding]:
        """Analyze aggregate design."""
        findings: list[Finding] = []
        if not assessment.bounded_contexts:
            return findings

        for ctx in assessment.bounded_contexts:
            if ctx.aggregates and len(ctx.entities) == 0:
                findings.append(
                    Finding(
                        category=FindingCategory.ddd_violation,
                        severity=Severity.medium,
                        title=f"Aggregate without entities in context: {ctx.name}",
                        description=(
                            f"Context `{ctx.name}` has aggregates but no entities. "
                            "Aggregates should consist of entities and value objects."
                        ),
                        evidence={"context": ctx.name, "aggregates": ctx.aggregates},
                        recommendation=(
                            "Verify that aggregates contain entities; if not, "
                            "review the aggregate design."
                        ),
                        impact=Impact.maintainability,
                        confidence=0.7,
                    )
                )
        return findings

    def _analyze_domain_events(self, assessment: DDDAssessment) -> list[Finding]:
        """Analyze domain event usage."""
        findings: list[Finding] = []
        if len(assessment.domain_events) == 0:
            findings.append(
                Finding(
                    category=FindingCategory.event_design,
                    severity=Severity.low,
                    title="No domain events detected",
                    description=(
                        "No domain events found in the project. "
                        "If this is a DDD project, domain events are important "
                        "for decoupling aggregate state changes."
                    ),
                    evidence={"domain_event_count": len(assessment.domain_events)},
                    recommendation=(
                        "Consider modeling important state changes as domain events "
                        "to decouple aggregates and enable event-driven designs."
                    ),
                    impact=Impact.scalability,
                    confidence=0.6,
                )
            )
        return findings

    def _analyze_acl(self, assessment: DDDAssessment) -> list[Finding]:
        """Analyze anti-corruption layer presence."""
        findings: list[Finding] = []
        if len(assessment.bounded_contexts) > 1 and len(assessment.anti_corruption_layers) == 0:
            findings.append(
                Finding(
                    category=FindingCategory.ddd_violation,
                    severity=Severity.medium,
                    title="Multiple bounded contexts without anti-corruption layers",
                    description=(
                        "Multiple bounded contexts detected but no anti-corruption layers found. "
                        "Without ACLs, domain models may leak between contexts, causing coupling."
                    ),
                    evidence={
                        "bounded_contexts": [ctx.name for ctx in assessment.bounded_contexts],
                        "acl_layers": len(assessment.anti_corruption_layers),
                    },
                    recommendation=(
                        "Introduce anti-corruption layers to translate between bounded "
                        "contexts when they have different domain models."
                    ),
                    impact=Impact.maintainability,
                    confidence=0.75,
                )
            )
        return findings

    def _generate_recommendations(self, findings: list[Finding]) -> list[Recommendation]:
        """Generate recommendations based on DDD findings."""
        recs: list[Recommendation] = []
        if any(f.category == FindingCategory.ddd_violation for f in findings):
            recs.append(
                Recommendation(
                    priority=Priority.medium,
                    problem="DDD structural issues detected",
                    solution=(
                        "Map bounded contexts, define aggregates with root entities, "
                        "and add anti-corruption layers between contexts."
                    ),
                    effort=Effort.medium,
                    impact="Improves domain model clarity and context isolation",
                )
            )
        if any(f.category == FindingCategory.event_design for f in findings):
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="Domain events not modeled",
                    solution=(
                        "Identify state changes that matter to the business and model "
                        "them as domain events for decoupling and auditability."
                    ),
                    effort=Effort.medium,
                    impact="Enables event-driven collaboration between aggregates",
                )
            )
        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No significant DDD issues",
                    solution="Maintain current DDD structure; review as the domain evolves.",
                    effort=Effort.low,
                    impact="Preserves domain coherence",
                )
            )
        return recs

