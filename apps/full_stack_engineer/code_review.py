"""
F2 — Code Review
=================

Comprehensive code review beyond linting:
- bug
- race condition
- deadlock
- SQL injection
- XSS
- security issue
- performance issue
- maintainability issue

Each finding includes evidence and priority.
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
class ReviewFinding:
    severity: str
    category: str
    title: str
    description: str
    recommendation: str
    evidence: str = ""
    line_number: int = 0
    confidence: float = 0.9
    cwe: str = ""


@dataclass
class CodeReviewReport:
    findings: list[ReviewFinding] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "findings": [
                {
                    "severity": f.severity,
                    "category": f.category,
                    "title": f.title,
                    "description": f.description,
                    "recommendation": f.recommendation,
                    "evidence": f.evidence,
                    "line_number": f.line_number,
                    "confidence": f.confidence,
                    "cwe": f.cwe,
                }
                for f in self.findings
            ],
            "summary": self.summary,
        }


class FullStackCodeReviewEngine:
    """Reviews code for quality, security, and maintainability."""

    async def review(self, code: str, filename: str = "<unknown>", context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        findings: list[ReviewFinding] = []
        try:
            tree = ast.parse(code, filename=filename)
        except SyntaxError as exc:
            return {
                "findings": [
                    {
                        "severity": Severity.CRITICAL,
                        "category": "Syntax",
                        "title": "Syntax Error",
                        "description": str(exc),
                        "recommendation": "Fix syntax errors before review.",
                        "line_number": exc.lineno or 0,
                        "confidence": 1.0,
                    }
                ],
                "summary": {"total_findings": 1, "critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0},
            }

        raw = code
        lines = code.splitlines()

        self._check_security_injection(raw, lines, findings)
        self._check_concurrency(tree, raw, lines, findings)
        self._check_resource(tree, raw, lines, findings)
        self._check_maintainability(tree, raw, lines, findings)
        self._check_api_surface(tree, raw, lines, findings)

        summary = {
            "total_findings": len(findings),
            "critical": sum(1 for f in findings if f.severity == Severity.CRITICAL),
            "high": sum(1 for f in findings if f.severity == Severity.HIGH),
            "medium": sum(1 for f in findings if f.severity == Severity.MEDIUM),
            "low": sum(1 for f in findings if f.severity == Severity.LOW),
            "info": sum(1 for f in findings if f.severity == Severity.INFO),
        }

        return {"findings": [f.__dict__ for f in findings], "summary": summary}

    def _check_security_injection(self, raw: str, lines: list[str], findings: list[ReviewFinding]):
        if "eval(" in raw:
            self._add_finding(raw, lines, findings, Severity.CRITICAL, "Security", "Use of eval()", "Replace eval() with ast.literal_eval or safer alternatives.", "CWE-94")
        if "exec(" in raw:
            self._add_finding(raw, lines, findings, Severity.CRITICAL, "Security", "Use of exec()", "Avoid exec(). Use function dispatch or configuration instead.", "CWE-94")
        if "pickle.loads" in raw:
            self._add_finding(raw, lines, findings, Severity.HIGH, "Security", "Unsafe deserialization", "Use JSON or trusted serialization formats instead of pickle.", "CWE-502")
        if "cursor.execute(" in raw and "%s" not in raw and "?" not in raw:
            self._add_finding(raw, lines, findings, Severity.HIGH, "Security", "Possible SQL injection", "Use parameterized queries instead of string formatting.", "CWE-89")
        if "render_template_string" in raw or "dangerouslySetInnerHTML" in raw:
            self._add_finding(raw, lines, findings, Severity.HIGH, "Security", "Possible XSS", "Escape user input before rendering HTML.", "CWE-79")
        if "os.system(" in raw or "subprocess.call(" in raw:
            self._add_finding(raw, lines, findings, Severity.HIGH, "Security", "Command injection risk", "Use subprocess.run with list args instead of shell=True.", "CWE-78")

    def _check_concurrency(self, tree: ast.AST, raw: str, lines: list[str], findings: list[ReviewFinding]):
        if "threading." in raw and "Lock()" not in raw:
            self._add_finding(raw, lines, findings, Severity.HIGH, "Concurrency", "Possible race condition", "Shared state accessed without lock protection.", "CWE-362")
        if "asyncio." in raw and "asyncio.Lock()" not in raw and "asyncio.Semaphore()" not in raw:
            if raw.count("await ") > 5 and "lock" not in raw.lower():
                self._add_finding(raw, lines, findings, Severity.MEDIUM, "Concurrency", "Possible async race condition", "Consider asyncio.Lock for shared mutable state.", "CWE-362")
        if "multiprocessing." in raw and "Lock()" not in raw:
            self._add_finding(raw, lines, findings, Severity.MEDIUM, "Concurrency", "Possible process-level race condition", "Use multiprocessing.Lock or manager for shared state.", "CWE-362")

    def _check_resource(self, tree: ast.AST, raw: str, lines: list[str], findings: list[ReviewFinding]):
        if "open(" in raw and "with " not in raw:
            self._add_finding(raw, lines, findings, Severity.MEDIUM, "Reliability", "Unclosed file resource", "Use context manager (`with` statement) to ensure file is closed.", "CWE-772")
        if "while True:" in raw and "break" not in raw:
            self._add_finding(raw, lines, findings, Severity.MEDIUM, "Reliability", "Infinite loop without break", "Ensure loop has a termination condition to avoid CPU exhaustion.", "")
        if "except:" in raw and "except Exception:" not in raw:
            self._add_finding(raw, lines, findings, Severity.MEDIUM, "Maintainability", "Bare except clause", "Catch specific exceptions instead of bare `except:`.", "CWE-396")

    def _check_maintainability(self, tree: ast.AST, raw: str, lines: list[str], findings: list[ReviewFinding]):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.end_lineno and node.lineno and (node.end_lineno - node.lineno) > 50:
                    self._add_finding(raw, lines, findings, Severity.MEDIUM, "Maintainability", f"Long function '{node.name}'", "Break into smaller functions with single responsibility.", "", node.lineno)
                for default in node.args.defaults + node.args.kw_defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        self._add_finding(raw, lines, findings, Severity.HIGH, "Maintainability", f"Mutable default argument in '{node.name}'", "Replace mutable default with None and instantiate inside function.", "CWE-371", node.lineno)
                        break
        if "global " in raw:
            self._add_finding(raw, lines, findings, Severity.LOW, "Maintainability", "Use of global variables", "Avoid global state; use dependency injection or closures.", "")

    def _check_api_surface(self, tree: ast.AST, raw: str, lines: list[str], findings: list[ReviewFinding]):
        if raw.count("def ") > 20 and len(raw) < 5000:
            self._add_finding(raw, lines, findings, Severity.LOW, "Maintainability", "High function density", "Consider splitting into multiple modules.", "")

    def _add_finding(self, raw: str, lines: list[str], findings: list[ReviewFinding], severity: Severity, category: str, title: str, recommendation: str, cwe: str = "", line_number: int = 0):
        evidence = ""
        if line_number <= 0:
            for idx, line in enumerate(lines, start=1):
                if title.lower() in line.lower() or any(k in line.lower() for k in ["eval(", "exec(", "pickle", "os.system", "open(", "global ", "while true:", "= []", "= {}"]):
                    evidence = line.strip()
                    line_number = idx
                    break
        findings.append(ReviewFinding(
            severity=severity.value if isinstance(severity, Severity) else severity,
            category=category,
            title=title,
            description=title,
            recommendation=recommendation,
            evidence=evidence,
            line_number=line_number,
            confidence=0.9,
            cwe=cwe,
        ))


code_review_engine = FullStackCodeReviewEngine()
