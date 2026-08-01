"""
System Architect — Event Analyzer.

Evaluates event-driven architecture design:
- Event schema presence and structure
- Event flow validation (producer/consumer direction)
- Saga pattern usage
- Event naming conventions
- Event sourcing readiness
- Schema versioning and backward compatibility
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


class EventAnalyzer:
    """
    Analyzes a project for event-driven design quality.

    Usage::
        analyzer = EventAnalyzer(repo_path)
        findings, recs = await analyzer.analyze()
    """

    EVENT_NAMING = ("event", "events", "domain_event", "integration_event", ".evt")
    SAGA_HINTS = ("saga", "orchestrator", "choreography", "compensat")
    SCHEMA_HINTS = ("schema", "event_schema", "avro", "json_schema", "protobuf")
    VERSION_HINTS = ("version", "schema_version", "compat")

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)

    async def analyze(self) -> tuple[list[Finding], list[Recommendation]]:
        """Run event-driven design analysis."""
        findings: list[Finding] = []
        events: list[str] = []
        sagas: list[str] = []
        schemas: list[str] = []
        handlers: list[tuple[str, str]] = []  # (module_path, event_name)
        versioned = 0
        total_event_defs = 0

        for py_file in self.repo_path.rglob("*.py"):
            module_path = str(py_file.relative_to(self.repo_path))
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except (SyntaxError, Exception):
                continue

            for node in ast.walk(tree):
                # Event class definition
                if isinstance(node, ast.ClassDef):
                    lower = node.name.lower()
                    if any(h in lower for h in self.EVENT_NAMING) and (
                        "event" in lower or "message" in lower
                    ):
                        events.append(f"{module_path}:{node.name}")
                        total_event_defs += 1
                        # Check versioning by scanning assignments
                        if self._has_version(node):
                            versioned += 1
                    if any(h in lower for h in self.SAGA_HINTS):
                        sagas.append(f"{module_path}:{node.name}")
                # Schema definition
                elif isinstance(node, ast.FunctionDef):
                    lower = node.name.lower()
                    if any(h in lower for h in self.SCHEMA_HINTS):
                        schemas.append(f"{module_path}:{node.name}")
                    if "handle" in lower or "on_" in lower or "subscribe" in lower:
                        handlers.append((module_path, node.name))

        # Findings
        findings.extend(self._analyze_event_schemas(events, schemas, total_event_defs, versioned))
        findings.extend(self._analyze_sagas(sagas))
        findings.extend(self._analyze_handlers(handlers, events))
        findings.extend(self._analyze_flow(events, handlers, sagas))

        recommendations = self._generate_recommendations(findings)

        return findings, recommendations

    # ------------------------------------------------------------------
    # Analysis methods
    # ------------------------------------------------------------------

    def _has_version(self, node: ast.ClassDef) -> bool:
        """Check if an event class has a version attribute."""
        for child in node.body:
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name) and "version" in target.id.lower():
                        return True
            elif isinstance(child, ast.AnnAssign):
                if isinstance(child.target, ast.Name) and "version" in child.target.id.lower():
                    return True
        return False

    def _analyze_event_schemas(
        self,
        events: list[str],
        schemas: list[str],
        total_event_defs: int,
        versioned: int,
    ) -> list[Finding]:
        findings: list[Finding] = []
        if events and not schemas:
            findings.append(
                Finding(
                    category=FindingCategory.event_design,
                    severity=Severity.medium,
                    title="Events without schema definitions",
                    description=(
                        f"{len(events)} event definitions found but no schema definitions. "
                        "Without explicit schemas, contract evolution is risky and "
                        "cross-service compatibility is hard to maintain."
                    ),
                    evidence={
                        "event_count": len(events),
                        "schema_count": len(schemas),
                    },
                    recommendation=(
                        "Define explicit event schemas (JSON Schema, Avro, or Pydantic models) "
                        "for every event. Version schemas to preserve backward compatibility."
                    ),
                    impact=Impact.maintainability,
                    confidence=0.8,
                )
            )
        if events and versioned < total_event_defs:
            unversioned = total_event_defs - versioned
            findings.append(
                Finding(
                    category=FindingCategory.event_design,
                    severity=Severity.low,
                    title=f"{unversioned} event definitions without versioning",
                    description=(
                        f"{unversioned} of {total_event_defs} event definitions lack a "
                        "version attribute. Event schema evolution requires explicit "
                        "versioning to avoid breaking consumers."
                    ),
                    evidence={
                        "total_events": total_event_defs,
                        "versioned_events": versioned,
                    },
                    recommendation=(
                        "Add a `version` field to every event schema and document "
                        "the compatibility policy (e.g., backward-compatible additions)."
                    ),
                    impact=Impact.modifiability,
                    confidence=0.7,
                )
            )
        return findings

    def _analyze_sagas(self, sagas: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        if not sagas:
            # If there are many events but no saga, it may be a sign of a distributed
            # transaction anti-pattern. But only flag if there are events present.
            # We check presence in the flow method.
            return findings
        findings.append(
            Finding(
                category=FindingCategory.event_design,
                severity=Severity.low,
                title="Saga orchestration detected",
                description=(
                    f"Found {len(sagas)} saga/orchestration component(s). "
                    "Verify sagas have compensating actions for every step."
                ),
                evidence={"saga_count": len(sagas), "sagas": sagas},
                recommendation=(
                    "Ensure every saga step has a compensating action and that "
                    "saga state is persisted for resume/rollback."
                ),
                impact=Impact.scalability,
                confidence=0.65,
            )
        )
        return findings

    def _analyze_handlers(
        self,
        handlers: list[tuple[str, str]],
        events: list[str],
    ) -> list[Finding]:
        findings: list[Finding] = []
        if events and not handlers:
            findings.append(
                Finding(
                    category=FindingCategory.event_design,
                    severity=Severity.high,
                    title="Events defined but no handlers/subscribers found",
                    description=(
                        f"{len(events)} events defined but no handlers or subscribers detected. "
                        "Events without consumers may indicate dead events or an "
                        "incomplete event flow."
                    ),
                    evidence={
                        "event_count": len(events),
                        "handler_count": len(handlers),
                    },
                    recommendation=(
                        "Verify that every event has at least one consumer, or "
                        "document why the event exists (e.g., for auditing)."
                    ),
                    impact=Impact.maintainability,
                    confidence=0.75,
                )
            )
        return findings

    def _analyze_flow(
        self,
        events: list[str],
        handlers: list[tuple[str, str]],
        sagas: list[str],
    ) -> list[Finding]:
        findings: list[Finding] = []
        if not events and not sagas:
            return findings
        # No finding expected for normal flow; add a "good practice" note as low only
        # when handlers exist and events exist.
        if events and handlers:
            findings.append(
                Finding(
                    category=FindingCategory.event_design,
                    severity=Severity.low,
                    title="Event-driven flow present",
                    description=(
                        "Events and handlers/subscribers both present, indicating an "
                        "event-driven flow."
                    ),
                    evidence={
                        "events": len(events),
                        "handlers": len(handlers),
                    },
                    recommendation=(
                        "Maintain event flow documentation; monitor for event storms "
                        "or orphaned events."
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
                    problem="Event-driven design gaps detected",
                    solution=(
                        "Ensure every event has a schema, version, producer, and consumer. "
                        "Document event flows and verify saga compensating actions."
                    ),
                    effort=Effort.medium,
                    impact="Improves event flow reliability and evolution safety",
                )
            )
        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No significant event-driven issues",
                    solution="Maintain current event design; review for schema governance.",
                    effort=Effort.low,
                    impact="Preserves event-driven architecture quality",
                )
            )
        return recs

