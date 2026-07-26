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

    def _check_solid(self, code_ast: CodeAST) -> list[CodeIssue]:
        """Check for SOLID principle violations."""
        issues = []
        raw = "\n".join(code_ast.raw_lines)

        # Single Responsibility Principle: Classes with too many methods
        for cls in code_ast.classes:
            num_methods = len(cls.methods)
            if num_methods > 15:
                issues.append(CodeIssue(
                    severity=Severity.HIGH,
                    category="SOLID",
                    description=f"Class '{cls.name}' has {num_methods} methods - violates Single Responsibility",
                    recommendation="Split class into smaller, focused classes",
                    line_number=cls.lineno,
                    confidence=0.85,
                ))

        # Open/Closed Principle: Large if-elif chains (feature envy)
        for func in code_ast.functions:
            if "elif" in raw and func.name not in ("__init__", "__new__"):
                lines = [l for l in code_ast.raw_lines if f"elif" in l]
                if len(lines) > 3:
                    issues.append(CodeIssue(
                        severity=Severity.MEDIUM,
                        category="SOLID",
                        description=f"Function '{func.name}' has multiple elif branches - consider Strategy pattern (Open/Closed)",
                        recommendation="Use strategy pattern or polymorphism instead of conditionals",
                        line_number=func.lineno,
                        confidence=0.7,
                    ))

        # Liskov Substitution: Check for mutable defaults
        if " = []" in raw or " = {}" in raw:
            issues.append(CodeIssue(
                severity=Severity.HIGH,
                category="SOLID",
                description="Mutable default arguments violate Liskov Substitution",
                recommendation="Use None as default and instantiate inside function",
                line_number=1,
                confidence=0.95,
            ))

        return issues

    def _check_ddd(self, code_ast: CodeAST) -> list[CodeIssue]:
        """Check for Domain-Driven Design patterns."""
        issues = []

        # Check for Entity patterns (classes with identity/id)
        for cls in code_ast.classes:
            has_id_attr = any("id" in method.name.lower() or "uuid" in method.name.lower()
                             for method in cls.methods)
            has_init = any(method.name == "__init__" for method in cls.methods)

            # Recommendation for Entity pattern
            if has_init and not has_id_attr:
                issues.append(CodeIssue(
                    severity=Severity.INFO,
                    category="DDD",
                    description=f"Class '{cls.name}' could be an Entity - consider adding identity field",
                    recommendation="Add 'id' or 'uuid' field for Entity pattern",
                    line_number=cls.lineno,
                    confidence=0.6,
                ))

            # Value Object: Check for __eq__ without side effects
            has_eq = any(method.name == "__eq__" for method in cls.methods)
            if has_eq and not has_id_attr:
                issues.append(CodeIssue(
                    severity=Severity.INFO,
                    category="DDD",
                    description=f"Class '{cls.name}' implements __eq__ without identity - could be Value Object",
                    recommendation="Consider making this class immutable",
                    line_number=cls.lineno,
                    confidence=0.5,
                ))

        return issues


code_analyzer = CodeAnalyzer()
