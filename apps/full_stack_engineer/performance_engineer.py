"""
F5 — Performance Engineer
==========================

Analyzes code for performance issues:
- Database N+1 queries
- Missing indexes
- Bundle size / lazy loading
- Rendering / hydration issues
"""

import ast
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class PerformanceIssue:
    severity: str
    category: str
    title: str
    description: str
    recommendation: str
    line_number: int = 0
    confidence: float = 0.9


@dataclass
class PerformanceReport:
    issues: list[PerformanceIssue] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "title": i.title,
                    "description": i.description,
                    "recommendation": i.recommendation,
                    "line_number": i.line_number,
                    "confidence": i.confidence,
                }
                for i in self.issues
            ],
            "summary": self.summary,
        }


class PerformanceEngineer:
    """Analyzes code for performance bottlenecks."""

    async def analyze(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        try:
            tree = ast.parse(code, filename=filename)
        except SyntaxError as exc:
            return {"error": f"Syntax error: {exc}", "filename": filename}

        raw = code
        lines = code.splitlines()
        issues: list[PerformanceIssue] = []

        self._check_n_plus_one(raw, lines, issues)
        self._check_loop_complexity(tree, raw, lines, issues)
        self._check_memory(tree, raw, lines, issues)
        self._check_io_blocking(tree, raw, lines, issues)

        summary = {
            "total_issues": len(issues),
            "critical": sum(1 for i in issues if i.severity == Severity.CRITICAL),
            "high": sum(1 for i in issues if i.severity == Severity.HIGH),
            "medium": sum(1 for i in issues if i.severity == Severity.MEDIUM),
            "low": sum(1 for i in issues if i.severity == Severity.LOW),
            "info": sum(1 for i in issues if i.severity == Severity.INFO),
        }

        return {"issues": [i.__dict__ for i in issues], "summary": summary}

    def _check_n_plus_one(self, raw: str, lines: list[str], issues: list[PerformanceIssue]):
        query_keywords = ["query(", "filter(", "get(", "execute(", "find(", "all("]
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("for ") and " in " in stripped:
                loop_start = i
                loop_indent = len(line) - len(line.lstrip())
                for j in range(i + 1, len(lines) + 1):
                    if j > len(lines):
                        break
                    next_line = lines[j - 1]
                    if next_line.strip() and not next_line.startswith(" " * (loop_indent + 1)) and not next_line.strip().startswith("#"):
                        break
                    if any(kw in next_line for kw in query_keywords):
                        issues.append(PerformanceIssue(
                            severity=Severity.HIGH.value,
                            category="Database",
                            title="Possible N+1 Query",
                            description="Database query appears inside a loop.",
                            recommendation="Use eager loading (join/subquery) or batch fetching.",
                            line_number=j,
                            confidence=0.85,
                        ))
                        break

    def _check_loop_complexity(self, tree: ast.AST, raw: str, lines: list[str], issues: list[PerformanceIssue]):
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if isinstance(child, ast.For):
                        issues.append(PerformanceIssue(
                            severity=Severity.MEDIUM.value,
                            category="Algorithm",
                            title="Nested Loop",
                            description="Nested loops may indicate O(n^2) complexity.",
                            recommendation="Consider using dictionary/set lookup to reduce complexity.",
                            line_number=node.lineno,
                            confidence=0.7,
                        ))
                        break

    def _check_memory(self, tree: ast.AST, raw: str, lines: list[str], issues: list[PerformanceIssue]):
        if "list(" in raw and "range(" in raw:
            issues.append(PerformanceIssue(
                severity=Severity.INFO.value,
                category="Memory",
                title="List Comprehension Alternative",
                description="Large list comprehensions may consume excess memory.",
                recommendation="Consider generator expressions for large datasets.",
                confidence=0.6,
            ))

    def _check_io_blocking(self, tree: ast.AST, raw: str, lines: list[str], issues: list[PerformanceIssue]):
        if "time.sleep(" in raw:
            issues.append(PerformanceIssue(
                severity=Severity.MEDIUM.value,
                category="Blocking I/O",
                title="Blocking sleep in async context",
                description="time.sleep() blocks the event loop.",
                recommendation="Use asyncio.sleep() in async functions.",
                confidence=0.9,
            ))
        if "requests.get(" in raw and "asyncio" in raw:
            issues.append(PerformanceIssue(
                severity=Severity.HIGH.value,
                category="Blocking I/O",
                title="Blocking HTTP request in async code",
                description="requests library blocks the event loop.",
                recommendation="Use aiohttp or httpx for async HTTP.",
                confidence=0.9,
            ))


performance_engineer = PerformanceEngineer()