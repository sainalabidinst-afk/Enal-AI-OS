"""
Architecture Patterns Knowledge
=================================

Implements RFC-0006 Code Knowledge Expansion:
- Clean Architecture: layer detection, dependency rule, boundaries
- DDD: bounded contexts, entities, value objects, aggregates, domain events
- SOLID: all 5 principles with detection logic
- CQRS: command/query separation, write/read models
- Event Sourcing: event store, replay, projection

This module produces structured findings about code architecture.
It does NOT modify code. It only analyzes and reports.
"""

import ast
import logging
from dataclasses import dataclass, field
from typing import Any

from apps.code_engineer.parser import CodeAST

logger = logging.getLogger(__name__)


class ArchitectureSeverity:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ArchitectureFinding:
    """A single architecture pattern finding."""
    category: str
    severity: str
    description: str
    recommendation: str
    line_number: int
    confidence: float = 1.0
    pattern: str = ""
    examples: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "recommendation": self.recommendation,
            "line_number": self.line_number,
            "confidence": round(self.confidence, 2),
            "pattern": self.pattern,
            "examples": self.examples,
        }


from apps.code_engineer.clean_architecture import CleanArchitectureAnalyzer
from apps.code_engineer.ddd_analysis import DDDAnalyzer
from apps.code_engineer.solid_analysis import SOLIDAnalyzer
from apps.code_engineer.cqrs_analysis import CQRSAnalyzer
from apps.code_engineer.event_sourcing_analysis import EventSourcingAnalyzer


class ArchitecturePatternAnalyzer:
    """
    Master analyzer that coordinates all architecture pattern analyses.
    """

    def __init__(self):
        self.clean_arch = CleanArchitectureAnalyzer()
        self.ddd = DDDAnalyzer()
        self.solid = SOLIDAnalyzer()
        self.cqrs = CQRSAnalyzer()
        self.event_sourcing = EventSourcingAnalyzer()

    def analyze(self, code_ast: CodeAST) -> dict[str, list[ArchitectureFinding]]:
        """Run all architecture pattern analyses."""
        return {
            "clean_architecture": self.clean_arch.analyze(code_ast),
            "ddd": self.ddd.analyze(code_ast),
            "solid": self.solid.analyze(code_ast),
            "cqrs": self.cqrs.analyze(code_ast),
            "event_sourcing": self.event_sourcing.analyze(code_ast),
        }

    def analyze_all(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        """Get all findings as a flat list."""
        results = self.analyze(code_ast)
        all_findings: list[ArchitectureFinding] = []
        for category_findings in results.values():
            all_findings.extend(category_findings)
        return all_findings


architecture_pattern_analyzer = ArchitecturePatternAnalyzer()
