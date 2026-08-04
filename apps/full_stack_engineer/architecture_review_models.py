"""
Architecture Review Models
============================

Data models, enums, and constants for the architecture review engine.
"""

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class Grade(str, Enum):
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"


class ArchitectureStyle(str, Enum):
    UNKNOWN = "unknown"
    CLEAN = "clean_architecture"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    MICROSERVICE = "microservice"
    EVENT_DRIVEN = "event_driven"
    CQRS = "cqrs"
    MONOLITH = "monolith"
    SERVERLESS = "serverless"
    MONOREPO = "monorepo"


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


LAYER_VIOLATION_PATTERNS: dict[str, list[dict[str, Any]]] = {
    "clean_architecture": [
        {
            "name": "domain_imports_infrastructure",
            "description": "Domain layer imports from infrastructure",
            "rule": "domain/.* should not import from infrastructure",
            "severity": Severity.CRITICAL,
            "check": lambda f, imports: "domain" in f.lower() and any("infrastructure" in i for i in imports),
        },
        {
            "name": "use_case_imports_framework",
            "description": "Use case / application layer imports framework code",
            "rule": "application/.* should not import framework-specific modules",
            "severity": Severity.HIGH,
            "check": lambda f, imports: ("application" in f.lower() or "use_case" in f.lower()) and any(
                fw in str(imports).lower() for fw in ["fastapi", "django", "flask", "sqlalchemy", "redis"]
            ),
        },
        {
            "name": "api_imports_core",
            "description": "API layer directly imports core domain instead of application",
            "rule": "api/.* should import from application not domain directly",
            "severity": Severity.MEDIUM,
            "check": lambda f, imports: "api" in f.lower() and any(
                "domain" in i and "entity" in i for i in imports
            ),
        },
    ],
    "layered": [
        {
            "name": "presentation_imports_data",
            "description": "Presentation layer imports data layer",
            "rule": "presentation/.* should not import from data/.* directly",
            "severity": Severity.CRITICAL,
            "check": lambda f, imports: ("presentation" in f.lower() or "controller" in f.lower()) and any(
                "data" in i or "repository" in i for i in imports
            ),
        },
        {
            "name": "service_imports_presentation",
            "description": "Service layer imports presentation layer",
            "rule": "service/.* should not import from presentation/.*",
            "severity": Severity.HIGH,
            "check": lambda f, imports: "service" in f.lower() and any(
                "controller" in i or "view" in i for i in imports
            ),
        },
    ],
    "hexagonal": [
        {
            "name": "core_imports_adapter",
            "description": "Core domain imports adapter",
            "rule": "core/.* should not import from adapter/.*",
            "severity": Severity.CRITICAL,
            "check": lambda f, imports: "core" in f.lower() and any(
                "adapter" in i for i in imports
            ),
        },
    ],
    "microservice": [
        {
            "name": "service_imports_another_service",
            "description": "Service imports from another service's internal modules",
            "rule": "services/.* should only communicate via API contracts",
            "severity": Severity.HIGH,
            "check": lambda f, imports: "service" in f.lower() and any(
                "service" in i and "shared" not in i and "contract" not in i for i in imports
            ),
        },
    ],
}

DEFAULT_VIOLATION_PATTERNS = [
    {
        "name": "utils_imports_all",
        "description": "Utility module imports from too many domains",
        "rule": "utils/.* should be dependency-free",
        "severity": Severity.MEDIUM,
        "check": lambda f, imports: "util" in f.lower() and len(imports) > 10,
    },
]


@dataclass
class ModuleInfo:
    """Information about a single module/file in the repository."""
    path: str
    lines_of_code: int
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    is_package: bool = False
    is_test: bool = False
    has_docstring: bool = False
    todo_count: int = 0
    fixme_count: int = 0
    complexity_score: float = 0.0


@dataclass
class DependencyEdge:
    """A dependency relationship between two modules."""
    source: str
    target: str
    is_circular: bool = False
    weight: float = 1.0


@dataclass
class CircularDependency:
    """A detected circular dependency chain."""
    modules: list[str]
    confidence: float = 1.0


@dataclass
class LayerViolation:
    """A detected layer violation."""
    module_path: str
    violation_type: str
    description: str
    severity: str
    source_layer: str
    target_layer: str
    imports: list[str]
    recommendation: str = ""


@dataclass
class CouplingMetric:
    """Coupling metrics for a module."""
    module_path: str
    ce: int = 0
    ca: int = 0
    instability: float = 0.0
    abstractness: float = 0.0
    distance: float = 0.0
    is_abstract: bool = False
    is_main: bool = False


@dataclass
class TechDebtItem:
    """A technical debt item."""
    module_path: str
    type: str
    description: str
    line: int = 0
    estimated_effort: str = "low"
    impact: str = "low"


@dataclass
class ADREntry:
    """An Architecture Decision Record entry."""
    title: str
    status: str
    date: str = ""
    decision: str = ""
    context: str = ""
    consequences: str = ""


@dataclass
class RefactoringRecommendation:
    """A prioritized refactoring recommendation."""
    priority: int
    title: str
    description: str
    rationale: str
    effort: str
    risk: str
    impact: str
    affected_modules: list[str] = field(default_factory=list)
    suggested_approach: str = ""


@dataclass
class ArchitectureReport:
    """Complete architecture analysis report."""

    repo_path: str = ""
    repo_name: str = ""
    total_modules: int = 0
    total_files: int = 0
    total_lines: int = 0

    architecture_score: float = 0.0
    layering_grade: Grade = Grade.C
    dependency_grade: Grade = Grade.C
    modularity_grade: Grade = Grade.C
    tech_debt_grade: Grade = Grade.C
    test_health_grade: Grade = Grade.C

    detected_style: str = "unknown"
    style_confidence: float = 0.0

    modules: list[ModuleInfo] = field(default_factory=list)

    dependency_edges: list[DependencyEdge] = field(default_factory=list)
    circular_dependencies: list[CircularDependency] = field(default_factory=list)
    total_dependencies: int = 0

    layer_violations: list[LayerViolation] = field(default_factory=list)
    layer_count: int = 0

    coupling_metrics: list[CouplingMetric] = field(default_factory=list)
    avg_instability: float = 0.0
    max_instability_modules: list[str] = field(default_factory=list)

    tech_debt_items: list[TechDebtItem] = field(default_factory=list)
    tech_debt_density: float = 0.0
    todo_count: int = 0
    fixme_count: int = 0

    adr_entries: list[ADREntry] = field(default_factory=list)
    adr_consistency_score: float = 0.0

    overall_risk: str = "low"
    maintenance_risk: str = "low"
    scalability_risk: str = "low"
    testability_risk: str = "low"
    deployability_risk: str = "low"
    risk_factors: list[str] = field(default_factory=list)

    recommendations: list[RefactoringRecommendation] = field(default_factory=list)

    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "architecture_score": round(self.architecture_score, 1),
            "layering_grade": self.layering_grade.value,
            "dependency_grade": self.dependency_grade.value,
            "modularity_grade": self.modularity_grade.value,
            "tech_debt_grade": self.tech_debt_grade.value,
            "test_health_grade": self.test_health_grade.value,
            "detected_style": self.detected_style,
            "style_confidence": round(self.style_confidence, 2),
            "arch": {
                "score": round(self.architecture_score, 1),
                "layering_grade": self.layering_grade.value,
                "dependency_grade": self.dependency_grade.value,
                "modularity_grade": self.modularity_grade.value,
                "tech_debt_grade": self.tech_debt_grade.value,
                "test_health_grade": self.test_health_grade.value,
                "detected_style": self.detected_style,
                "style_confidence": round(self.style_confidence, 2),
            },
            "repo": {
                "path": self.repo_path,
                "name": self.repo_name,
                "total_modules": self.total_modules,
                "total_files": self.total_files,
                "total_lines": self.total_lines,
            },
            "layer": {
                "violations": [
                    {
                        "module": v.module_path,
                        "type": v.violation_type,
                        "description": v.description,
                        "severity": v.severity,
                        "source_layer": v.source_layer,
                        "target_layer": v.target_layer,
                        "recommendation": v.recommendation,
                    }
                    for v in self.layer_violations
                ],
                "total_violations": len(self.layer_violations),
                "layer_count": self.layer_count,
            },
            "dependency": {
                "total_edges": len(self.dependency_edges),
                "circular": [
                    {"modules": c.modules, "confidence": c.confidence}
                    for c in self.circular_dependencies
                ],
                "total_circular": len(self.circular_dependencies),
            },
            "coupling": [
                {
                    "module": m.module_path,
                    "ce": m.ce,
                    "ca": m.ca,
                    "instability": round(m.instability, 2),
                    "abstractness": round(m.abstractness, 2),
                    "distance": round(m.distance, 2),
                }
                for m in self.coupling_metrics
            ],
            "tech_debt": {
                "items": [
                    {
                        "module": t.module_path,
                        "type": t.type,
                        "description": t.description,
                        "line": t.line,
                        "effort": t.estimated_effort,
                        "impact": t.impact,
                    }
                    for t in self.tech_debt_items
                ],
                "total_items": len(self.tech_debt_items),
                "density": round(self.tech_debt_density, 4),
                "todo_count": self.todo_count,
                "fixme_count": self.fixme_count,
            },
            "risk": {
                "overall": self.overall_risk,
                "maintenance": self.maintenance_risk,
                "scalability": self.scalability_risk,
                "testability": self.testability_risk,
                "deployability": self.deployability_risk,
                "factors": self.risk_factors,
            },
            "recommendations": [
                {
                    "priority": r.priority,
                    "title": r.title,
                    "description": r.description,
                    "rationale": r.rationale,
                    "effort": r.effort,
                    "risk": r.risk,
                    "impact": r.impact,
                    "affected_modules": r.affected_modules,
                    "suggested_approach": r.suggested_approach,
                }
                for r in sorted(self.recommendations, key=lambda x: x.priority)
            ],
            "summary": {
                "strengths": self.strengths,
                "weaknesses": self.weaknesses,
                "text": self.summary,
            },
        }

    def to_markdown(self) -> str:
        lines = [
            "# Architecture Report",
            "",
            f"**Repository**: {self.repo_name or self.repo_path}",
            f"**Architecture Score**: **{self.architecture_score:.1f}/100** ({self.layering_grade.value})",
            f"**Detected Style**: {self.detected_style.title().replace('_', ' ')} (confidence: {self.style_confidence:.0%})",
            f"**Total Modules**: {self.total_modules} | **Files**: {self.total_files} | **Lines**: {self.total_lines:,}",
            "",
            "---",
            "",
            "## Architecture Scores",
            "",
            "| Metric | Grade |",
            "|--------|-------|",
            f"| Layering | {self.layering_grade.value} |",
            f"| Dependency | {self.dependency_grade.value} |",
            f"| Modularity | {self.modularity_grade.value} |",
            f"| Technical Debt | {self.tech_debt_grade.value} |",
            f"| Test Health | {self.test_health_grade.value} |",
            "",
            "---",
            "",
            "## Strengths",
            "",
        ]
        for s in (self.strengths or ["None identified"]):
            lines.append(f"- ✅ {s}")
        lines += [
            "",
            "## Weaknesses",
            "",
        ]
        for w in (self.weaknesses or ["None identified"]):
            lines.append(f"- ⚠️ {w}")
        lines += [
            "",
            "---",
            "",
            "## Layer Violations",
            "",
        ]
        if self.layer_violations:
            lines.append(f"**Total**: {len(self.layer_violations)}")
            lines.append("")
            lines.append("| Module | Type | Severity | Source → Target |")
            lines.append("|--------|------|----------|-----------------|")
            for v in self.layer_violations[:20]:
                lines.append(f"| `{v.module_path}` | {v.violation_type} | {v.severity} | {v.source_layer} → {v.target_layer} |")
            if len(self.layer_violations) > 20:
                lines.append(f"| ... and {len(self.layer_violations) - 20} more |")
        else:
            lines.append("✅ No layer violations detected.")
        lines += [
            "",
            "---",
            "",
            "## Circular Dependencies",
            "",
        ]
        if self.circular_dependencies:
            lines.append(f"**Total**: {len(self.circular_dependencies)}")
            for cd in self.circular_dependencies:
                modules_str = " → ".join(cd.modules)
                lines.append(f"- `{modules_str}`")
        else:
            lines.append("✅ No circular dependencies detected.")
        lines += [
            "",
            "---",
            "",
            "## Risk Assessment",
            "",
            f"**Overall**: {self.overall_risk.upper()}",
            f"- Maintenance: {self.maintenance_risk}",
            f"- Scalability: {self.scalability_risk}",
            f"- Testability: {self.testability_risk}",
            f"- Deployability: {self.deployability_risk}",
            "",
        ]
        if self.risk_factors:
            lines.append("**Risk Factors:**")
            for rf in self.risk_factors:
                lines.append(f"- {rf}")
        lines += [
            "",
            "---",
            "",
            "## Top Recommendations",
            "",
        ]
        if self.recommendations:
            for r in sorted(self.recommendations, key=lambda x: x.priority)[:10]:
                lines.append(f"### {r.priority}. {r.title}")
                lines.append(f"**Effort**: {r.effort} | **Risk**: {r.risk} | **Impact**: {r.impact}")
                lines.append(f"**Description**: {r.description}")
                lines.append(f"**Rationale**: {r.rationale}")
                if r.affected_modules:
                    lines.append(f"**Affected**: `{', '.join(r.affected_modules[:5])}`")
                if r.suggested_approach:
                    lines.append(f"**Approach**: {r.suggested_approach}")
                lines.append("")
        else:
            lines.append("No recommendations generated.")
        lines += [
            "---",
            "",
            "## Summary",
            "",
            self.summary or "No summary generated.",
        ]
        return "\n".join(lines)
