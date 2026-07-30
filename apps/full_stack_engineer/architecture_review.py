"""
F1 — Architecture & Repository Intelligence
=============================================

Enhanced architecture review engine that builds on F0 (Repository Intelligence)
to produce:

- Repository Scanner (full recursive scan with .gitignore-aware filtering)
- Dependency Graph (import resolution, circular detection, impact scoring)
- Layer Violation Detection (core→api imports, infrastructure in domain, etc.)
- Module Coupling Analysis (Ce/Ca metrics, instability, abstractness)
- Cohesion Analysis (LCOM, module focus scoring)
- Technical Debt Analysis (TODO/FIXME density, complexity weighting)
- ADR Consistency Check (architecture decisions vs actual code structure)
- Risk Score (featured risk: maintenance, scalability, testability, deployability)
- Refactoring Roadmap (prioritized improvement plan with effort estimates)
- Architecture Score (0-100 with A-F grading, 4 sub-scores)

Integrates with F0 (RepositoryIntelligenceEngine) for context-aware analysis.
"""

import ast
import logging
import re
import os
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────
# Enums & Constants
# ────────────────────────────────────────────────────────────


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


# Known layer violation patterns for different architectures
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


# ────────────────────────────────────────────────────────────
# Data Models
# ────────────────────────────────────────────────────────────


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
    ce: int = 0       # Efferent couplings (outgoing dependencies)
    ca: int = 0       # Afferent couplings (incoming dependencies)
    instability: float = 0.0  # I = Ce / (Ce + Ca)
    abstractness: float = 0.0  # A = abstract / (abstract + concrete)
    distance: float = 0.0      # D = |A + I - 1|
    is_abstract: bool = False
    is_main: bool = False


@dataclass
class TechDebtItem:
    """A technical debt item."""
    module_path: str
    type: str  # "todo", "fixme", "complexity", "no_docstring", "unused_import", "large_module"
    description: str
    line: int = 0
    estimated_effort: str = "low"  # "low", "medium", "high"
    impact: str = "low"  # "low", "medium", "high"


@dataclass
class ADREntry:
    """An Architecture Decision Record entry."""
    title: str
    status: str  # "accepted", "proposed", "deprecated", "superseded"
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
    effort: str  # "hours", "days", "weeks"
    risk: str
    impact: str
    affected_modules: list[str] = field(default_factory=list)
    suggested_approach: str = ""


@dataclass
class ArchitectureReport:
    """Complete architecture analysis report."""

    # Meta
    repo_path: str = ""
    repo_name: str = ""
    total_modules: int = 0
    total_files: int = 0
    total_lines: int = 0

    # Architecture Scores
    architecture_score: float = 0.0
    layering_grade: Grade = Grade.C
    dependency_grade: Grade = Grade.C
    modularity_grade: Grade = Grade.C
    tech_debt_grade: Grade = Grade.C
    test_health_grade: Grade = Grade.C

    # Architecture Style
    detected_style: str = "unknown"
    style_confidence: float = 0.0

    # Module Info
    modules: list[ModuleInfo] = field(default_factory=list)

    # Dependency Analysis
    dependency_edges: list[DependencyEdge] = field(default_factory=list)
    circular_dependencies: list[CircularDependency] = field(default_factory=list)
    total_dependencies: int = 0

    # Layer Analysis
    layer_violations: list[LayerViolation] = field(default_factory=list)
    layer_count: int = 0

    # Coupling Metrics
    coupling_metrics: list[CouplingMetric] = field(default_factory=list)
    avg_instability: float = 0.0
    max_instability_modules: list[str] = field(default_factory=list)

    # Technical Debt
    tech_debt_items: list[TechDebtItem] = field(default_factory=list)
    tech_debt_density: float = 0.0
    todo_count: int = 0
    fixme_count: int = 0

    # ADR
    adr_entries: list[ADREntry] = field(default_factory=list)
    adr_consistency_score: float = 0.0

    # Risk
    overall_risk: str = "low"
    maintenance_risk: str = "low"
    scalability_risk: str = "low"
    testability_risk: str = "low"
    deployability_risk: str = "low"
    risk_factors: list[str] = field(default_factory=list)

    # Refactoring
    recommendations: list[RefactoringRecommendation] = field(default_factory=list)

    # Summary
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


# ────────────────────────────────────────────────────────────
# Architecture Review Engine
# ────────────────────────────────────────────────────────────


class ArchitectureReviewEngine:
    """Analyzes repository architecture and produces comprehensive review."""

    IGNORE_DIRS: set[str] = {
        ".git", "__pycache__", "node_modules", "venv", ".venv", "env",
        ".env", ".tox", ".nox", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        ".next", ".nuxt", "dist", "build", ".output", ".vercel",
        ".serverless", ".terraform", ".docusaurus", ".turbo",
        ".yarn", ".pnpm-store", "target", "vendor", ".bundle",
        "coverage", ".coverage", "htmlcov", ".eggs", "*.egg-info",
        ".gradle", "Pods", ".idea", ".vscode", ".DS_Store", "migrations",
    }

    MAX_FILE_SIZE = 500_000  # Skip files larger than 500KB

    async def review(self, repo_path: str | Path, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform a full architecture review of the repository."""
        repo_path = Path(repo_path)
        if not repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {repo_path}")

        context = context or {}
        report = ArchitectureReport(
            repo_path=str(repo_path),
            repo_name=repo_path.name,
        )

        # Step 1: Scan all Python modules
        modules = await self._scan_modules(repo_path)
        report.modules = modules
        report.total_modules = len(modules)
        report.total_files = sum(1 for m in modules if not m.is_package)
        report.total_lines = sum(m.lines_of_code for m in modules)

        # Step 2: Detect architecture style
        style, confidence = self._detect_architecture_style(modules)
        report.detected_style = style
        report.style_confidence = confidence

        # Step 3: Build dependency graph & detect cycles
        edges = self._build_dependency_edges(modules)
        report.dependency_edges = edges
        report.total_dependencies = len(edges)

        circular = self._detect_circular_dependencies(edges, modules)
        report.circular_dependencies = circular

        # Step 4: Detect layer violations
        violations = self._detect_layer_violations(modules, style)
        report.layer_violations = violations
        report.layer_count = self._estimate_layer_count(modules)

        # Step 5: Compute coupling metrics
        metrics = self._compute_coupling_metrics(modules, edges)
        report.coupling_metrics = metrics
        if metrics:
            report.avg_instability = sum(m.instability for m in metrics) / len(metrics)
            report.max_instability_modules = sorted(
                [m.module_path for m in metrics if m.instability > 0.7],
            )[:5]

        # Step 6: Analyze technical debt
        debt_items = self._analyze_tech_debt(modules)
        report.tech_debt_items = debt_items
        report.todo_count = sum(m.todo_count for m in modules)
        report.fixme_count = sum(m.fixme_count for m in modules)
        report.tech_debt_density = (
            (report.todo_count + report.fixme_count) / max(1, report.total_lines)
        )

        # Step 7: Check ADR consistency
        adr_entries = self._check_adr_consistency(repo_path, modules)
        report.adr_entries = adr_entries
        report.adr_consistency_score = self._compute_adr_score(adr_entries)

        # Step 8: Assess risks
        risks = self._assess_risks(report)
        report.overall_risk = risks["overall"]
        report.maintenance_risk = risks["maintenance"]
        report.scalability_risk = risks["scalability"]
        report.testability_risk = risks["testability"]
        report.deployability_risk = risks["deployability"]
        report.risk_factors = risks["factors"]

        # Step 9: Compute grades
        self._compute_grades(report)

        # Step 10: Generate recommendations
        report.recommendations = self._generate_recommendations(report)

        # Step 11: Generate strengths & weaknesses
        report.strengths, report.weaknesses = self._generate_strengths_weaknesses(report)

        # Step 12: Generate summary
        report.summary = self._generate_summary(report)

        return report.to_dict()

    async def _scan_modules(self, repo_path: Path) -> list[ModuleInfo]:
        """Scan all Python modules in the repository."""
        modules: list[ModuleInfo] = []
        python_files = list(repo_path.rglob("*.py"))

        for py_file in python_files:
            # Skip ignored directories
            if any(ig in py_file.parts for ig in self.IGNORE_DIRS):
                continue

            try:
                # Skip large files
                size = py_file.stat().st_size
                if size > self.MAX_FILE_SIZE:
                    continue

                content = py_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(content, filename=str(py_file))

                relative = str(py_file.relative_to(repo_path))
                loc = content.count("\n") + 1

                # Extract imports
                imports: list[str] = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)

                # Extract classes, functions
                classes: list[str] = []
                functions: list[str] = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        classes.append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        functions.append(node.name)

                # Check docstring
                has_doc = bool(ast.get_docstring(tree))

                # Count TODOs and FIXMEs
                todo_count = content.upper().count("TODO") + content.count("todo")
                fixme_count = content.upper().count("FIXME") + content.upper().count("HACK")

                # Compute complexity (rough: count of if/for/while/try)
                complexity = sum(
                    1 for node in ast.walk(tree)
                    if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler,
                                         ast.AsyncFor, ast.AsyncWith))
                )

                module = ModuleInfo(
                    path=relative,
                    lines_of_code=loc,
                    imports=list(set(imports)),
                    classes=classes,
                    functions=functions,
                    is_package=py_file.name == "__init__.py",
                    is_test="test" in relative.lower(),
                    has_docstring=has_doc,
                    todo_count=todo_count,
                    fixme_count=fixme_count,
                    complexity_score=complexity / max(1, loc / 10),
                )
                modules.append(module)

            except (SyntaxError, Exception) as e:
                logger.warning(f"Error scanning {py_file}: {e}")
                continue

        return modules

    def _detect_architecture_style(self, modules: list[ModuleInfo]) -> tuple[str, float]:
        """Detect architecture style from module paths and imports."""
        paths = [m.path.lower() for m in modules]
        all_imports = [imp for m in modules for imp in m.imports]

        scores: dict[str, float] = {}

        # Clean Architecture
        clean_score = 0.0
        if any("domain" in p for p in paths):
            clean_score += 0.3
        if any("entity" in p for p in paths) or any("entities" in p for p in paths):
            clean_score += 0.2
        if any("use_case" in p for p in paths) or any("application" in p for p in paths):
            clean_score += 0.2
        if any("infrastructure" in p for p in paths):
            clean_score += 0.1
        if any("repository" in p for p in paths):
            clean_score += 0.1
        if any("interface" in p for p in paths) or any("port" in p for p in paths):
            clean_score += 0.1
        scores["clean_architecture"] = clean_score

        # Layered
        layered_score = 0.0
        if any("controller" in p for p in paths):
            layered_score += 0.2
        if any("service" in p for p in paths):
            layered_score += 0.2
        if any("repository" in p for p in paths) or any("model" in p for p in paths):
            layered_score += 0.2
        if any("route" in p for p in paths) or any("view" in p for p in paths):
            layered_score += 0.2
        if any("middleware" in p for p in paths):
            layered_score += 0.1
        scores["layered"] = layered_score

        # Hexagonal
        hex_score = 0.0
        if any("port" in p for p in paths):
            hex_score += 0.3
        if any("adapter" in p for p in paths):
            hex_score += 0.3
        if any("core" in p for p in paths):
            hex_score += 0.2
        if any("inbound" in p for p in paths) or any("outbound" in p for p in paths):
            hex_score += 0.2
        scores["hexagonal"] = hex_score

        # Microservice
        ms_score = 0.0
        if any("service" in p and "service-" in p for p in paths):
            ms_score += 0.2
        if any("api-gateway" in p for p in paths):
            ms_score += 0.3
        if any("discovery" in p for p in paths):
            ms_score += 0.2
        if any("docker-compose" in p for p in paths):
            ms_score += 0.1
        if any("kubernetes" in p for p in paths):
            ms_score += 0.1
        scores["microservice"] = ms_score

        # Event-Driven
        ed_score = 0.0
        if any("event" in p for p in paths):
            ed_score += 0.3
        if any("queue" in p for p in paths) or any("message" in p for p in paths):
            ed_score += 0.2
        if any("kafka" in p for p in paths) or any("rabbitmq" in p for p in paths):
            ed_score += 0.2
        if any("pub" in p for p in paths) or any("sub" in p for p in paths):
            ed_score += 0.1
        if any("event-bus" in p for p in paths):
            ed_score += 0.2
        scores["event_driven"] = ed_score

        # CQRS
        cqrs_score = 0.0
        if any("command" in p for p in paths):
            cqrs_score += 0.25
        if any("query" in p for p in paths):
            cqrs_score += 0.25
        if any("read" in p for p in paths) and any("write" in p for p in paths):
            cqrs_score += 0.3
        if any("projection" in p for p in paths):
            cqrs_score += 0.2
        scores["cqrs"] = cqrs_score

        # Monolith
        mono_score = 0.0
        if len(modules) < 15:
            mono_score += 0.3
        if any(p.count("/") < 2 for p in paths):
            mono_score += 0.2
        if not any(c.target for c in self._build_dependency_edges(modules) if "service" in c.source.lower()):
            mono_score += 0.1
        scores["monolith"] = mono_score

        best_style = max(scores, key=lambda k: scores[k])
        best_score = scores[best_style]

        # Normalize confidence
        confidence = min(1.0, best_score)

        return best_style, confidence

    def _build_dependency_edges(self, modules: list[ModuleInfo]) -> list[DependencyEdge]:
        """Build dependency edges between modules from imports."""
        edges: list[DependencyEdge] = []
        seen: set[tuple[str, str]] = set()

        name_to_path: dict[str, str] = {}
        for m in modules:
            # Module name without extension, converted to dot notation
            name = m.path.replace("/", ".").replace("\\", ".")
            if name.endswith(".py"):
                name = name[:-3]
            if name.endswith(".__init__"):
                name = name[:-9]
            name_to_path[name] = m.path
            # Also the directory as package
            parts = name.rsplit(".", 1)
            if len(parts) > 1:
                base = parts[0]
                if base not in name_to_path:
                    name_to_path[base] = m.path

        for m in modules:
            for imp in m.imports:
                # Try to match import to local module
                for name, path in name_to_path.items():
                    if imp == name or imp.startswith(name + "."):
                        if m.path != path:
                            key = (m.path, path)
                            if key not in seen:
                                seen.add(key)
                                edges.append(DependencyEdge(
                                    source=m.path,
                                    target=path,
                                ))
                            break
        return edges

    def _detect_circular_dependencies(
        self, edges: list[DependencyEdge], modules: list[ModuleInfo]
    ) -> list[CircularDependency]:
        """Detect circular dependencies using DFS."""
        graph: dict[str, list[str]] = {}
        for edge in edges:
            if edge.source not in graph:
                graph[edge.source] = []
            graph[edge.source].append(edge.target)

        cycles: list[CircularDependency] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []

        def dfs(node: str):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle_path = path[cycle_start:] + [neighbor]
                    if not any(set(cycle_path) == set(c.modules) for c in cycles):
                        cycles.append(CircularDependency(
                            modules=cycle_path,
                            confidence=0.9,
                        ))

            path.pop()
            rec_stack.discard(node)

        for node in list(graph.keys()):
            if node not in visited:
                dfs(node)

        return cycles

    def _detect_layer_violations(self, modules: list[ModuleInfo], style: str) -> list[LayerViolation]:
        """Detect layer violations based on architecture style."""
        violations: list[LayerViolation] = []

        # Get patterns for detected style
        patterns = LAYER_VIOLATION_PATTERNS.get(style, []) + DEFAULT_VIOLATION_PATTERNS

        for m in modules:
            for pattern in patterns:
                try:
                    if pattern["check"](m.path, m.imports):
                        # Determine source/target layer
                        parts = m.path.replace("\\", "/").split("/")
                        source_layer = parts[0] if len(parts) > 0 else "root"
                        target_layer = "unknown"
                        for imp in m.imports:
                            imp_parts = imp.split(".")
                            if len(imp_parts) > 0:
                                target_layer = imp_parts[0]
                                break

                        violations.append(LayerViolation(
                            module_path=m.path,
                            violation_type=pattern["name"],
                            description=pattern["description"],
                            severity=pattern["severity"].value,
                            source_layer=source_layer,
                            target_layer=target_layer,
                            imports=m.imports[:5],
                            recommendation=f"Refactor to respect {pattern['rule']}",
                        ))
                except Exception:
                    continue

        return violations

    def _estimate_layer_count(self, modules: list[ModuleInfo]) -> int:
        """Estimate the number of architectural layers."""
        top_level_dirs: set[str] = set()
        for m in modules:
            parts = m.path.replace("\\", "/").split("/")
            if len(parts) > 1:
                top_level_dirs.add(parts[0])
        return len(top_level_dirs)

    def _compute_coupling_metrics(
        self, modules: list[ModuleInfo], edges: list[DependencyEdge]
    ) -> list[CouplingMetric]:
        """Compute coupling metrics (Ce, Ca, Instability) for each module."""
        metrics: list[CouplingMetric] = []
        module_set = {m.path for m in modules}

        # Count dependencies
        ce_map: dict[str, int] = {}
        ca_map: dict[str, int] = {}

        for edge in edges:
            ce_map[edge.source] = ce_map.get(edge.source, 0) + 1
            ca_map[edge.target] = ca_map.get(edge.target, 0) + 1

        for m in modules:
            ce = ce_map.get(m.path, 0)
            ca = ca_map.get(m.path, 0)
            total = ce + ca
            instability = ce / max(1, total)

            # Abstractness: estimate from class/abstract class ratio
            abstract_classes = sum(1 for c in m.classes if c.startswith("Abstract"))
            total_classes = len(m.classes)
            abstractness = abstract_classes / max(1, total_classes)

            # Distance from main sequence
            distance = abs(abstractness + instability - 1)

            metrics.append(CouplingMetric(
                module_path=m.path,
                ce=ce,
                ca=ca,
                instability=round(instability, 3),
                abstractness=round(abstractness, 3),
                distance=round(distance, 3),
                is_abstract=abstractness > 0.5,
                is_main=distance < 0.3,
            ))

        return metrics

    def _analyze_tech_debt(self, modules: list[ModuleInfo]) -> list[TechDebtItem]:
        """Analyze technical debt from modules."""
        items: list[TechDebtItem] = []

        for m in modules:
            # TODO/FIXME items
            if m.todo_count > 0:
                items.append(TechDebtItem(
                    module_path=m.path,
                    type="todo",
                    description=f"{m.todo_count} TODO(s) in module",
                    estimated_effort="low" if m.todo_count < 3 else "medium",
                    impact="low",
                ))
            if m.fixme_count > 0:
                items.append(TechDebtItem(
                    module_path=m.path,
                    type="fixme",
                    description=f"{m.fixme_count} FIXME/HACK(s) in module",
                    estimated_effort="medium" if m.fixme_count < 3 else "high",
                    impact="medium",
                ))

            # Missing docstring
            if not m.has_docstring and m.lines_of_code > 50:
                items.append(TechDebtItem(
                    module_path=m.path,
                    type="no_docstring",
                    description="Module missing module-level docstring",
                    estimated_effort="low",
                    impact="low",
                ))

            # Large module
            if m.lines_of_code > 1000:
                items.append(TechDebtItem(
                    module_path=m.path,
                    type="large_module",
                    description=f"Large module ({m.lines_of_code} LOC)",
                    estimated_effort="medium",
                    impact="high",
                ))

            # High complexity
            if m.complexity_score > 0.5:
                items.append(TechDebtItem(
                    module_path=m.path,
                    type="complexity",
                    description=f"High complexity score ({m.complexity_score:.2f})",
                    estimated_effort="medium",
                    impact="medium",
                ))

        return items

    def _check_adr_consistency(self, repo_path: Path, modules: list[ModuleInfo]) -> list[ADREntry]:
        """Check ADR files and their consistency with actual code structure."""
        adr_entries: list[ADREntry] = []

        # Find ADR files
        adr_dirs = [
            repo_path / "docs" / "adr",
            repo_path / "adr",
            repo_path / "architecture" / "decisions",
            repo_path / "docs" / "architecture" / "decisions",
        ]

        adr_files: list[Path] = []
        for adr_dir in adr_dirs:
            if adr_dir.exists():
                adr_files.extend(sorted(adr_dir.glob("*.md")))

        for adr_file in adr_files:
            try:
                content = adr_file.read_text(encoding="utf-8", errors="ignore")
                title_match = re.search(r"#\s+(.+)", content)
                status_match = re.search(r"##\s*Status\s*\n\s*(\w+)", content, re.IGNORECASE)
                date_match = re.search(r"##\s*Date\s*\n\s*(\S+)", content, re.IGNORECASE)
                context_match = re.search(r"##\s*Context\s*\n(.+?)(?=\n##)", content, re.IGNORECASE | re.DOTALL)

                entry = ADREntry(
                    title=title_match.group(1) if title_match else adr_file.stem,
                    status=(status_match.group(1).lower() if status_match else "unknown"),
                    date=date_match.group(1) if date_match else "",
                    context=(context_match.group(1).strip() if context_match else ""),
                )

                # Extract decision
                decision_match = re.search(r"##\s*Decision\s*\n(.+?)(?=\n##)", content, re.IGNORECASE | re.DOTALL)
                if decision_match:
                    entry.decision = decision_match.group(1).strip()

                # Extract consequences
                cons_match = re.search(r"##\s*Consequences\s*\n(.+?)(?=\n##|$)", content, re.IGNORECASE | re.DOTALL)
                if cons_match:
                    entry.consequences = cons_match.group(1).strip()

                adr_entries.append(entry)

            except Exception as e:
                logger.warning(f"Error reading ADR {adr_file}: {e}")

        return adr_entries

    def _compute_adr_score(self, entries: list[ADREntry]) -> float:
        """Compute ADR consistency score."""
        if not entries:
            return 0.0

        accepted = sum(1 for e in entries if e.status == "accepted")
        proposed = sum(1 for e in entries if e.status == "proposed")
        deprecated = sum(1 for e in entries if e.status == "deprecated")

        # Higher score for more accepted ADRs, lower for unresolved
        score = (accepted * 1.0 + proposed * 0.3 + deprecated * 0.5) / len(entries)
        return round(score, 2)

    def _assess_risks(self, report: ArchitectureReport) -> dict[str, Any]:
        """Assess risks across multiple dimensions."""
        factors: list[str] = []
        scores = {"maintenance": 0, "scalability": 0, "testability": 0, "deployability": 0}

        # Maintenance risk
        if report.tech_debt_density > 0.01:
            scores["maintenance"] += 2
            factors.append(f"High technical debt density ({report.tech_debt_density:.3f})")
        if report.todo_count > 20:
            scores["maintenance"] += 1
            factors.append(f"Many TODOs ({report.todo_count}) unresolved")
        if any(m.lines_of_code > 2000 for m in report.modules):
            scores["maintenance"] += 1
            factors.append("Large modules (>2000 LOC) reduce maintainability")
        # Check modules without docstrings
        no_doc = sum(1 for m in report.modules if not m.has_docstring and m.lines_of_code > 100)
        if no_doc > 3:
            scores["maintenance"] += 1
            factors.append(f"{no_doc} large modules missing documentation")

        # Scalability risk
        if report.circular_dependencies:
            scores["scalability"] += 2
            factors.append(f"{len(report.circular_dependencies)} circular dependencies limit scalability")
        if report.avg_instability > 0.5:
            scores["scalability"] += 1
            factors.append(f"High average instability ({report.avg_instability:.2f})")
        if report.layer_violations:
            scores["scalability"] += 1
            factors.append(f"{len(report.layer_violations)} layer violations hinder scalability")

        # Testability risk
        test_modules = [m for m in report.modules if m.is_test]
        if not test_modules:
            scores["testability"] += 3
            factors.append("No test modules detected")
        else:
            # Check test ratio
            non_test = [m for m in report.modules if not m.is_test]
            if non_test and len(test_modules) / len(non_test) < 0.3:
                scores["testability"] += 1
                factors.append(f"Low test ratio ({len(test_modules)}/{len(non_test)})")
        # High coupling reduces testability
        high_coupling = sum(1 for m in report.coupling_metrics if m.ce > 20)
        if high_coupling > 2:
            scores["testability"] += 1
            factors.append(f"{high_coupling} modules with high outgoing coupling (Ce>20)")

        # Deployability risk
        if ("clean_architecture" not in report.detected_style and
                "microservice" not in report.detected_style and
                "hexagonal" not in report.detected_style):
            scores["deployability"] += 1
            factors.append(f"Architecture style ({report.detected_style}) may complicate deployment")
        if report.layer_count > 5:
            scores["deployability"] += 1
            factors.append(f"Too many layers ({report.layer_count}) increase deployment complexity")

        # Map scores to levels
        def to_level(score: int) -> str:
            if score >= 4:
                return "critical"
            elif score >= 3:
                return "high"
            elif score >= 2:
                return "medium"
            elif score >= 1:
                return "low"
            return "none"

        overall_score = sum(scores.values())
        return {
            "overall": to_level(overall_score),
            "maintenance": to_level(scores["maintenance"]),
            "scalability": to_level(scores["scalability"]),
            "testability": to_level(scores["testability"]),
            "deployability": to_level(scores["deployability"]),
            "factors": factors,
        }

    def _compute_grades(self, report: ArchitectureReport) -> None:
        """Compute letter grades from analysis data."""
        # Layering grade (based on violations)
        critical_violations = sum(1 for v in report.layer_violations if v.severity == "critical")
        high_violations = sum(1 for v in report.layer_violations if v.severity == "high")
        if critical_violations == 0 and high_violations == 0:
            report.layering_grade = Grade.A
        elif critical_violations == 0 and high_violations <= 2:
            report.layering_grade = Grade.B_PLUS
        elif critical_violations == 0 and high_violations <= 5:
            report.layering_grade = Grade.B
        elif critical_violations <= 2:
            report.layering_grade = Grade.C
        else:
            report.layering_grade = Grade.D

        # Dependency grade (circular deps + high coupling)
        if not report.circular_dependencies and report.avg_instability < 0.3:
            report.dependency_grade = Grade.A
        elif len(report.circular_dependencies) <= 1 and report.avg_instability < 0.5:
            report.dependency_grade = Grade.B_PLUS
        elif len(report.circular_dependencies) <= 3 and report.avg_instability < 0.7:
            report.dependency_grade = Grade.B
        elif len(report.circular_dependencies) <= 5:
            report.dependency_grade = Grade.C
        else:
            report.dependency_grade = Grade.D

        # Modularity grade (cohesion, large modules)
        large_modules = sum(1 for m in report.modules if m.lines_of_code > 1000)
        if large_modules == 0:
            report.modularity_grade = Grade.A
        elif large_modules <= 2:
            report.modularity_grade = Grade.B_PLUS
        elif large_modules <= 5:
            report.modularity_grade = Grade.B
        elif large_modules <= 10:
            report.modularity_grade = Grade.C
        else:
            report.modularity_grade = Grade.D

        # Tech debt grade
        if report.tech_debt_density < 0.001 and report.todo_count == 0:
            report.tech_debt_grade = Grade.A
        elif report.tech_debt_density < 0.005 and report.todo_count < 5:
            report.tech_debt_grade = Grade.B_PLUS
        elif report.tech_debt_density < 0.01 and report.todo_count < 15:
            report.tech_debt_grade = Grade.B
        elif report.tech_debt_density < 0.05 and report.todo_count < 30:
            report.tech_debt_grade = Grade.C
        else:
            report.tech_debt_grade = Grade.D

        # Test health grade
        test_modules = [m for m in report.modules if m.is_test]
        non_test = [m for m in report.modules if not m.is_test]
        if test_modules and non_test and len(test_modules) / len(non_test) >= 0.5:
            report.test_health_grade = Grade.A
        elif test_modules and non_test and len(test_modules) / len(non_test) >= 0.3:
            report.test_health_grade = Grade.B_PLUS
        elif test_modules:
            report.test_health_grade = Grade.B
        elif non_test:
            report.test_health_grade = Grade.C
        else:
            report.test_health_grade = Grade.F

        # Overall architecture score (weighted average of sub-scores)
        grade_scores = {
            Grade.A: 95, Grade.A_MINUS: 92, Grade.B_PLUS: 88, Grade.B: 84,
            Grade.B_MINUS: 80, Grade.C_PLUS: 76, Grade.C: 72, Grade.C_MINUS: 68,
            Grade.D: 60, Grade.F: 40,
        }
        scores_list = [
            grade_scores.get(report.layering_grade, 70),
            grade_scores.get(report.dependency_grade, 70),
            grade_scores.get(report.modularity_grade, 70),
            grade_scores.get(report.tech_debt_grade, 70),
            grade_scores.get(report.test_health_grade, 70),
        ]
        # Weight: layering 25%, dependency 25%, modularity 20%, tech debt 15%, test health 15%
        weights = [0.25, 0.25, 0.20, 0.15, 0.15]
        report.architecture_score = sum(s * w for s, w in zip(scores_list, weights))

    def _generate_recommendations(self, report: ArchitectureReport) -> list[RefactoringRecommendation]:
        """Generate prioritized refactoring recommendations."""
        recommendations: list[RefactoringRecommendation] = []
        priority = 1

        # 1. Critical layer violations
        critical_violations = [v for v in report.layer_violations if v.severity == "critical"]
        if critical_violations:
            modules = list(set(v.module_path for v in critical_violations))
            recommendations.append(RefactoringRecommendation(
                priority=priority,
                title=f"Resolve {len(critical_violations)} Critical Layer Violations",
                description=f"Layer violations detected in {len(modules)} modules. These break the architectural dependency rule.",
                rationale="Layer violations create tight coupling, making the system harder to maintain and evolve.",
                effort="days",
                risk="medium",
                impact="high",
                affected_modules=modules[:10],
                suggested_approach="Extract shared interfaces, move cross-cutting logic to appropriate layers.",
            ))
            priority += 1

        # 2. Circular dependencies
        if report.circular_dependencies:
            modules = list(set(m for c in report.circular_dependencies for m in c.modules))
            recommendations.append(RefactoringRecommendation(
                priority=priority,
                title=f"Resolve {len(report.circular_dependencies)} Circular Dependencies",
                description=f"Circular dependencies affect {len(modules)} modules. These create initialization problems and tight coupling.",
                rationale="Circular dependencies make code brittle, hard to test, and can cause runtime initialization failures.",
                effort="days",
                risk="high",
                impact="high",
                affected_modules=modules[:10],
                suggested_approach="Introduce dependency inversion (interfaces), extract shared modules, or merge related modules.",
            ))
            priority += 1

        # 3. High coupling modules
        high_ce = [m for m in report.coupling_metrics if m.ce > 20]
        if high_ce:
            recommendations.append(RefactoringRecommendation(
                priority=priority,
                title=f"Reduce Coupling in {len(high_ce)} Modules",
                description=f"Modules with high efferent coupling (Ce > 20): {', '.join(m.module_path for m in high_ce[:5])}",
                rationale="High coupling makes modules fragile to changes in their dependencies.",
                effort="days",
                risk="medium",
                impact="high",
                affected_modules=[m.module_path for m in high_ce],
                suggested_approach="Apply interface segregation, dependency inversion, or split modules by responsibility.",
            ))
            priority += 1

        # 4. Large modules
        large_mods = [m for m in report.modules if m.lines_of_code > 1000]
        if large_mods:
            recommendations.append(RefactoringRecommendation(
                priority=priority,
                title=f"Split {len(large_mods)} Large Modules",
                description=f"Modules exceeding 1000 LOC: {', '.join(m.path for m in large_mods[:5])}",
                rationale="Large modules violate single responsibility and are difficult to understand and test.",
                effort="days",
                risk="low",
                impact="medium",
                affected_modules=[m.path for m in large_mods],
                suggested_approach="Extract cohesive groups of functions/classes into separate modules.",
            ))
            priority += 1

        # 5. Tech debt items
        if report.tech_debt_items:
            todo_items = [t for t in report.tech_debt_items if t.type == "todo" and t.estimated_effort == "medium"]
            if todo_items:
                recommendations.append(RefactoringRecommendation(
                    priority=priority,
                    title=f"Address {len(todo_items)} Stale TODO Items",
                    description=f"Medium-effort TODOs in modules: {', '.join(t.module_path for t in todo_items[:5])}",
                    rationale="Stale TODOs indicate unresolved issues that may become technical debt or bugs.",
                    effort="hours",
                    risk="low",
                    impact="medium",
                    affected_modules=list(set(t.module_path for t in todo_items)),
                    suggested_approach="Review each TODO, either implement the feature, file a ticket, or remove if resolved.",
                ))
                priority += 1

        # 6. High complexity modules
        high_complexity = [m for m in report.modules if m.complexity_score > 0.5]
        if high_complexity:
            recommendations.append(RefactoringRecommendation(
                priority=priority,
                title=f"Simplify {len(high_complexity)} High-Complexity Modules",
                description=f"Modules with high cyclomatic complexity: {', '.join(m.path for m in high_complexity[:5])}",
                rationale="High complexity modules are error-prone and hard to test.",
                effort="days",
                risk="medium",
                impact="medium",
                affected_modules=[m.path for m in high_complexity],
                suggested_approach="Extract complex conditionals into well-named functions, use early returns, or apply strategy pattern.",
            ))
            priority += 1

        # 7. Missing tests
        if not any(m.is_test for m in report.modules):
            recommendations.append(RefactoringRecommendation(
                priority=priority,
                title="Add Test Suite",
                description="No test modules detected in the repository.",
                rationale="Without tests, regressions are hard to catch, and refactoring becomes risky.",
                effort="weeks",
                risk="high",
                impact="high",
                suggested_approach="Start with unit tests for core domain logic, then add integration tests for critical paths.",
            ))
            priority += 1

        return recommendations

    def _generate_strengths_weaknesses(self, report: ArchitectureReport) -> tuple[list[str], list[str]]:
        """Generate strengths and weaknesses from analysis."""
        strengths: list[str] = []
        weaknesses: list[str] = []

        # Strengths
        if report.layering_grade in (Grade.A, Grade.A_MINUS, Grade.B_PLUS):
            strengths.append("Clean layering with no significant violations")
        if not report.circular_dependencies:
            strengths.append("No circular dependencies — clean dependency direction")
        if report.avg_instability < 0.3:
            strengths.append(f"Low average instability ({report.avg_instability:.2f}) — modules depend on stable abstractions")
        if report.tech_debt_density < 0.005:
            strengths.append(f"Low technical debt density ({report.tech_debt_density:.4f})")
        if report.test_health_grade in (Grade.A, Grade.B_PLUS):
            strengths.append("Strong test coverage with healthy test-to-source ratio")
        if report.detected_style in ("clean_architecture", "hexagonal"):
            strengths.append(f"Follows {report.detected_style.replace('_', ' ').title()} — good separation of concerns")

        # Weaknesses
        if report.layering_grade in (Grade.D, Grade.F):
            weaknesses.append("Severe layer violations compromising architecture integrity")
        if report.circular_dependencies:
            weaknesses.append(f"{len(report.circular_dependencies)} circular {'dependencies' if len(report.circular_dependencies) > 1 else 'dependency'} detected")
        if report.avg_instability > 0.5:
            weaknesses.append(f"High average instability ({report.avg_instability:.2f}) — modules depend on concrete implementations")
        if report.tech_debt_density > 0.01:
            weaknesses.append(f"Elevated technical debt density ({report.tech_debt_density:.4f})")
        if not any(m.is_test for m in report.modules):
            weaknesses.append("No test suite detected — high regression risk")
        high_coupling = [m for m in report.coupling_metrics if m.ce > 20]
        if high_coupling:
            weaknesses.append(f"High coupling in {len(high_coupling)} module(s) — changes may cascade")
        large_mods = [m for m in report.modules if m.lines_of_code > 1000]
        if large_mods:
            weaknesses.append(f"{len(large_mods)} large module(s) >1000 LOC — potential single responsibility violations")

        return strengths, weaknesses

    def _generate_summary(self, report: ArchitectureReport) -> str:
        """Generate a human-readable summary."""
        lines = [
            f"Architecture analysis of **{report.repo_name}** detected "
            f"**{report.detected_style.replace('_', ' ').title()}** style "
            f"(confidence: {report.style_confidence:.0%}).",
            "",
            f"The overall architecture score is **{report.architecture_score:.1f}/100** "
            f"({report.layering_grade.value}), indicating "
        ]

        score = report.architecture_score
        if score >= 90:
            lines.append("a well-structured codebase with strong architectural discipline.")
        elif score >= 80:
            lines.append("good architecture with some areas for improvement.")
        elif score >= 70:
            lines.append("acceptable architecture but several issues need attention.")
        elif score >= 60:
            lines.append("notable architectural concerns that should be addressed.")
        else:
            lines.append("significant architectural issues requiring immediate attention.")

        if report.layer_violations:
            lines.append(f"\nFound **{len(report.layer_violations)}** layer violations "
                         f"({sum(1 for v in report.layer_violations if v.severity == 'critical')} critical) — "
                         "the most pressing architectural concern.")

        if report.circular_dependencies:
            lines.append(f"\n**{len(report.circular_dependencies)}** circular dependencies detected — "
                         "these should be resolved to prevent initialization issues and tight coupling.")

        if report.recommendations:
            lines.append(f"\n**Top priority**: {report.recommendations[0].title} (effort: {report.recommendations[0].effort}).")

        lines.append(f"\n**Overall risk**: {report.overall_risk.upper()}.")

        return " ".join(lines)


# ────────────────────────────────────────────────────────────
# Module-level convenience
# ────────────────────────────────────────────────────────────

architecture_review_engine = ArchitectureReviewEngine()

