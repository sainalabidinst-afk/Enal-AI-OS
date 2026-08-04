"""
F1 — Architecture & Repository Intelligence
============================================

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

from apps.full_stack_engineer.architecture_review_models import (
    ADREntry,
    ArchitectureReport,
    ArchitectureStyle,
    CircularDependency,
    CouplingMetric,
    DEFAULT_VIOLATION_PATTERNS,
    DependencyEdge,
    Grade,
    LayerViolation,
    LAYER_VIOLATION_PATTERNS,
    ModuleInfo,
    RefactoringRecommendation,
    RiskLevel,
    Severity,
    TechDebtItem,
)
from apps.full_stack_engineer.architecture_review_engine import ArchitectureReviewEngine

architecture_review_engine = ArchitectureReviewEngine()
