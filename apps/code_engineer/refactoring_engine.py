"""
Refactoring Engine
===================

Pattern-based code improvement suggestions for Python repositories.
Detects code smells, design pattern violations, performance anti-patterns,
SOLID principle violations, and type hint completeness.

Features:
- Code smell detection (long methods, too many params, duplicate code)
- Design pattern suggestions
- Performance anti-pattern detection
- SOLID principle violations
- Type hint completeness
"""

import ast
import logging
from pathlib import Path

from apps.code_engineer.refactoring_models import (
    RefactoringCategory,
    RefactoringReport,
    RefactoringSeverity,
    RefactoringSuggestion,
)
from apps.code_engineer.refactoring_rules import (
    check_bare_excepts,
    check_commented_code,
    check_deep_nesting,
    check_duplicate_code,
    check_large_module,
    check_long_class,
    check_long_methods,
    check_magic_numbers,
    check_missing_type_hints,
    check_mutable_defaults,
    check_single_letter_vars,
    check_string_concat,
    check_suggest_design_pattern,
    check_too_many_params,
    check_too_many_returns,
)

logger = logging.getLogger(__name__)


class RefactoringEngine:
    """Analyzes code and produces refactoring suggestions."""

    DESIGN_PATTERNS = {
        "singleton": ["__new__", "get_instance", "instance"],
        "factory": ["Factory", "create_", "build_", "_factory"],
        "observer": ["observ", "listener", "subscribe", "notify"],
        "strategy": ["Strategy", "strategy", "_algorithm"],
        "repository": ["Repository", "repository", "_repo"],
        "adapter": ["Adapter", "adapt", "wrapper"],
        "decorator": ["Decorator", "decorate", "_wrapper"],
        "builder": ["Builder", "build_"],
    }

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)

    async def analyze(self, module_paths: list[str] | None = None) -> RefactoringReport:
        """Analyze repository and generate refactoring suggestions."""
        suggestions: list[RefactoringSuggestion] = []

        if module_paths:
            py_files = [self.repo_path / p for p in module_paths]
        else:
            py_files = list(self.repo_path.rglob("*.py"))

        for py_file in py_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
                relative = str(py_file.relative_to(self.repo_path))
            except (SyntaxError, ValueError, Exception) as e:
                logger.warning(f"Skipping {py_file}: {e}")
                continue

            suggestions.extend(check_long_methods(tree, relative, content))
            suggestions.extend(check_too_many_params(tree, relative))
            suggestions.extend(check_long_class(tree, relative))
            suggestions.extend(check_missing_type_hints(tree, relative, content))
            suggestions.extend(check_too_many_returns(tree, relative))
            suggestions.extend(check_deep_nesting(tree, relative))
            suggestions.extend(check_magic_numbers(tree, relative, content))
            suggestions.extend(check_duplicate_code(tree, relative, content))
            suggestions.extend(check_large_module(tree, relative, str(self.repo_path)))
            suggestions.extend(check_string_concat(tree, relative, content))
            suggestions.extend(check_single_letter_vars(tree, relative))
            suggestions.extend(check_commented_code(tree, relative, content))
            suggestions.extend(check_mutable_defaults(tree, relative))
            suggestions.extend(check_bare_excepts(tree, relative))
            suggestions.extend(check_suggest_design_pattern(tree, relative, content))

        report = RefactoringReport(suggestions=suggestions)

        for s in suggestions:
            report.by_category[s.category] = report.by_category.get(s.category, 0) + 1
            report.by_severity[s.severity] = report.by_severity.get(s.severity, 0) + 1
            report.by_effort[s.effort] = report.by_effort.get(s.effort, 0) + 1

        report.total_suggestions = len(suggestions)

        report.top_priorities = sorted(
            [s for s in suggestions if s.severity in (RefactoringSeverity.CRITICAL, RefactoringSeverity.HIGH)],
            key=lambda s: s.confidence,
            reverse=True,
        )[:10]

        lines = [
            "# Refactoring Analysis Report",
            "",
            f"**Total Suggestions**: {report.total_suggestions}",
            "",
        ]
        for cat, count in sorted(report.by_category.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- **{cat}**: {count}")
        lines.append("")
        for sev, count in sorted(report.by_severity.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- **Severity {sev}**: {count}")
        report.summary = "\n".join(lines)

        return report
