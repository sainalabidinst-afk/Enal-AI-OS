"""
Code Engineer Analyzer
=======================

Analyzes Python code for quality, security, and best practices.
"""

import logging
from dataclasses import dataclass

from apps.code_engineer.parser import CodeAST

logger = logging.getLogger(__name__)


class Severity:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class CodeIssue:
    severity: str
    category: str
    description: str
    recommendation: str
    line_number: int
    confidence: float = 1.0


class CodeAnalyzer:
    """Analyzes Python code for issues."""

    def __init__(self):
        self._rules = [
            self._check_imports,
            self._check_docstrings,
            self._check_function_length,
            self._check_security,
            self._check_naming,
            self._check_solid,
            self._check_ddd,
        ]

    def analyze(self, code_ast: CodeAST) -> list[CodeIssue]:
        issues = []
        for rule in self._rules:
            try:
                issues.extend(rule(code_ast))
            except Exception as e:
                logger.error("Analysis rule failed: %s", e)
        return issues

    def _check_imports(self, code_ast: CodeAST) -> list[CodeIssue]:
        issues = []
        for imp in code_ast.imports:
            if imp.module == "os" or imp.module.startswith("os."):
                issues.append(CodeIssue(
                    severity=Severity.MEDIUM,
                    category="Security",
                    description="Use of os module may pose security risks",
                    recommendation="Review os module usage for path traversal or command injection",
                    line_number=1,
                    confidence=0.8,
                ))
        return issues

    def _check_docstrings(self, code_ast: CodeAST) -> list[CodeIssue]:
        issues = []
        for cls in code_ast.classes:
            if not cls.docstring:
                issues.append(CodeIssue(
                    severity=Severity.LOW,
                    category="Documentation",
                    description=f"Class {cls.name} is missing docstring",
                    recommendation="Add docstring to class",
                    line_number=cls.lineno,
                    confidence=1.0,
                ))
            for method in cls.methods:
                if not method.docstring:
                    issues.append(CodeIssue(
                        severity=Severity.LOW,
                        category="Documentation",
                        description=f"Method {method.name} in class {cls.name} is missing docstring",
                        recommendation="Add docstring to method",
                        line_number=method.lineno,
                        confidence=1.0,
                    ))
        for func in code_ast.functions:
            if not func.docstring:
                issues.append(CodeIssue(
                    severity=Severity.LOW,
                    category="Documentation",
                    description=f"Function {func.name} is missing docstring",
                    recommendation="Add docstring to function",
                    line_number=func.lineno,
                    confidence=1.0,
                ))
        return issues

    def _check_function_length(self, code_ast: CodeAST) -> list[CodeIssue]:
        issues = []
        for func in code_ast.functions:
            if func.lineno > 50:
                issues.append(CodeIssue(
                    severity=Severity.MEDIUM,
                    category="Complexity",
                    description=f"Function {func.name} is too long (line {func.lineno})",
                    recommendation="Consider breaking into smaller functions",
                    line_number=func.lineno,
                    confidence=0.7,
                ))
        return issues

    def _check_security(self, code_ast: CodeAST) -> list[CodeIssue]:
        issues = []
        raw = "\n".join(code_ast.raw_lines)
        if "eval(" in raw:
            issues.append(CodeIssue(
                severity=Severity.CRITICAL,
                category="Security",
                description="Use of eval() is dangerous",
                recommendation="Replace eval() with safer alternatives",
                line_number=raw.find("eval(") + 1,
                confidence=1.0,
            ))
        if "exec(" in raw:
            issues.append(CodeIssue(
                severity=Severity.CRITICAL,
                category="Security",
                description="Use of exec() is dangerous",
                recommendation="Replace exec() with safer alternatives",
                line_number=raw.find("exec(") + 1,
                confidence=1.0,
            ))
        if "pickle.loads" in raw:
            issues.append(CodeIssue(
                severity=Severity.HIGH,
                category="Security",
                description="Use of pickle.loads() is unsafe",
                recommendation="Use JSON or other safe serialization",
                line_number=raw.find("pickle.loads") + 1,
                confidence=0.9,
            ))
        return issues

    def _check_naming(self, code_ast: CodeAST) -> list[CodeIssue]:
        issues = []
        for func in code_ast.functions:
            if func.name.startswith("__") and func.name.endswith("__"):
                continue
            if func.name.isupper() and len(func.name) > 1:
                continue
            if "_" not in func.name and func.name[0].islower() and len(func.name) > 10:
                issues.append(CodeIssue(
                    severity=Severity.INFO,
                    category="Style",
                    description=f"Function {func.name} may benefit from snake_case",
                    recommendation="Consider using snake_case for function names",
                    line_number=func.lineno,
                    confidence=0.6,
                ))
        return issues


code_analyzer = CodeAnalyzer()
