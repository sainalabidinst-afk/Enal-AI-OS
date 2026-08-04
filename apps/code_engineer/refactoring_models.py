"""
Refactoring Models
===================

Shared data models for the refactoring engine and rules.
"""

from dataclasses import dataclass, field
from typing import Any


class RefactoringCategory:
    CODE_SMELL = "code_smell"
    DESIGN_PATTERN = "design_pattern"
    PERFORMANCE = "performance"
    SOLID = "solid"
    TYPE_HINT = "type_hint"
    STYLE = "style"
    SECURITY = "security"
    BEST_PRACTICE = "best_practice"


class RefactoringSeverity:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class RefactoringSuggestion:
    """A single refactoring suggestion."""
    category: str
    severity: str
    module_path: str
    line_number: int
    description: str
    problem: str
    suggestion: str
    confidence: float
    effort: str
    impact: str
    example_before: str = ""
    example_after: str = ""
    references: list[str] = field(default_factory=list)


@dataclass
class RefactoringReport:
    """Complete refactoring analysis report."""
    suggestions: list[RefactoringSuggestion] = field(default_factory=list)
    total_suggestions: int = 0
    by_category: dict[str, int] = field(default_factory=dict)
    by_severity: dict[str, int] = field(default_factory=dict)
    by_effort: dict[str, int] = field(default_factory=dict)
    top_priorities: list[RefactoringSuggestion] = field(default_factory=list)
    summary: str = ""
