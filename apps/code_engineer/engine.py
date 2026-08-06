"""
Code Engineer Engine
====================

Domain engine orchestrator for the Code Engineer Capability Pack.

Orchestrates:
    1. Code parsing and analysis
    2. Architecture pattern detection
    3. Secure coding analysis
    4. Dependency graph building
    5. Refactoring suggestions
    6. Patch generation
    7. Test generation
    8. Regression risk analysis

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from typing import Any

from apps.code_engineer.parser import code_parser, CodeAST
from apps.code_engineer.analyzer import code_analyzer, CodeAnalyzer
from apps.code_engineer.architecture_patterns import (
    architecture_pattern_analyzer,
    ArchitecturePatternAnalyzer,
)
from apps.code_engineer.secure_coding import (
    secure_coding_analyzer,
    SecureCodingAnalyzer,
)
from apps.code_engineer.dependency_graph import DependencyGraphBuilder
from apps.code_engineer.architecture_reader import ArchitectureReader, read_architecture
from apps.code_engineer.refactoring_engine import RefactoringEngine
from apps.code_engineer.patch_generator import PatchGenerator
from apps.code_engineer.regression_analyzer import RegressionAnalyzer
from apps.code_engineer.test_generator import TestGenerator

logger = logging.getLogger(__name__)


class CodeEngineerEngine:
    """
    Orchestrates the full code engineering pipeline.

    Public API::

        engine = CodeEngineerEngine()
        report = engine.review(code, filename="app.py", language="python")
    """

    def __init__(self) -> None:
        self._parser = code_parser
        self._analyzer = code_analyzer
        self._arch_pattern_analyzer = architecture_pattern_analyzer
        self._secure_coding_analyzer = secure_coding_analyzer
        self._components_loaded = False
        self._repo_path: str | None = None

    async def _ensure_components(self) -> None:
        if self._components_loaded:
            return
        self._dep_builder_cls = DependencyGraphBuilder
        self._arch_reader_cls = ArchitectureReader
        self._arch_reader_fn = read_architecture
        self._refactor_cls = RefactoringEngine
        self._patch_cls = PatchGenerator
        self._regression_cls = RegressionAnalyzer
        self._test_cls = TestGenerator
        self._repo_path = tempfile.mkdtemp()
        self._components_loaded = True

    def review(
        self,
        code: str,
        filename: str = "<unknown>",
        language: str = "python",
    ) -> dict[str, Any]:
        """Run full code review: quality + security + architecture."""
        code_ast = self._parser.parse(code, filename=filename)
        issues = self._analyzer.analyze(code_ast)

        arch_results = self._arch_pattern_analyzer.analyze(code_ast)
        arch_findings = [
            {
                "category": f"architecture.{f.category}",
                "pattern": f.pattern,
                "severity": f.severity,
                "description": f.description,
                "recommendation": f.recommendation,
                "line": f.line_number,
                "confidence": f.confidence,
            }
            for category, findings in arch_results.items()
            for f in findings
        ]

        sec_results = self._secure_coding_analyzer.analyze(code_ast)
        sec_findings = [
            {
                "category": f"security.{f.category}",
                "pattern": f.pattern,
                "severity": f.severity,
                "description": f.description,
                "recommendation": f.recommendation,
                "line": f.line_number,
                "confidence": f.confidence,
            }
            for category, findings in sec_results.items()
            for f in findings
        ]

        return {
            "task": "review",
            "filename": filename,
            "language": language,
            "functions": len(code_ast.functions),
            "classes": len(code_ast.classes),
            "issues": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "line": issue.line_number,
                    "confidence": issue.confidence,
                }
                for issue in issues
            ],
            "architecture_patterns": {
                "total_findings": len(arch_findings),
                "findings": arch_findings,
            },
            "secure_coding": {
                "total_findings": len(sec_findings),
                "findings": sec_findings,
            },
        }

    async def analyze_repository(self, repo_path: str) -> dict[str, Any]:
        """Run full repository analysis pipeline."""
        await self._ensure_components()
        path = os.path.abspath(repo_path)
        if not os.path.exists(path):
            return {"error": f"Repository path not found: {repo_path}"}

        self._repo_path = path
        reader = self._arch_reader_cls(path)
        architecture = await reader.read()
        if not architecture:
            return {"error": "Architecture analysis failed"}

        dep_builder = self._dep_builder_cls(path)
        dep_summary = await dep_builder.build()

        return {
            "task": "analyze_repository",
            "architecture": architecture,
            "dependency_graph": {
                "total_modules": dep_summary.total_modules,
                "total_dependencies": dep_summary.total_dependencies,
                "circular_dependencies": len(dep_summary.circular_dependencies),
                "orphan_modules": dep_summary.orphan_modules,
            },
        }

    async def get_refactoring_suggestions(
        self, code: str, filename: str = "<unknown>"
    ) -> dict[str, Any]:
        """Get refactoring suggestions for code."""
        await self._ensure_components()
        self._parser.parse(code, filename=filename)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file = os.path.join(tmpdir, filename)
            await asyncio.to_thread(self._write_file_sync, tmp_file, code)
            engine = self._refactor_cls(tmpdir)
            report = await engine.analyze([filename])
            return {
                "filename": filename,
                "suggestions": [
                    {
                        "severity": s.severity,
                        "category": s.category,
                        "description": s.description,
                        "recommendation": s.suggestion,
                        "line": s.line_number,
                        "confidence": s.confidence,
                    }
                    for s in report.suggestions
                ],
            }

    async def generate_patch(
        self, original: str, modified: str, filename: str
    ) -> dict[str, Any]:
        """Generate a rollback-ready patch between two versions."""
        await self._ensure_components()
        gen = self._patch_cls(self._repo_path or ".")
        bundle = await gen.generate_from_changes(
            file_path=filename,
            old_content=original,
            new_content=modified,
        )
        diff = bundle.to_unified_diff()
        is_valid = await gen.validate_patch(bundle)
        return {
            "filename": filename,
            "patch_id": bundle.patch_id,
            "diff": diff,
            "diff_type": "unified",
            "is_valid": is_valid,
        }

    async def generate_tests(
        self, source_path: str, module_path: str
    ) -> dict[str, Any]:
        """Generate tests for a Python module."""
        await self._ensure_components()
        gen = self._test_cls()
        test_file = await gen.generate_for_module(
            source_path=source_path,
            module_path=module_path,
        )
        return {
            "file_path": test_file.file_path,
            "total_tests": len(test_file.tests),
            "edge_cases": len(test_file.edge_case_tests),
            "coverage_estimate": round(test_file.coverage_estimate, 2),
            "fixtures": len(test_file.fixtures),
        }

    async def analyze_regression_risk(
        self, repo_path: str, changes: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Analyze regression risk for a set of changes."""
        await self._ensure_components()
        analyzer = self._regression_cls()
        report = await analyzer.analyze_changes(
            repo_path=repo_path,
            changes=changes,
        )
        return report.to_dict()

    @staticmethod
    def _write_file_sync(path: str, content: str) -> None:
        """Synchronous file write helper."""
        with open(path, "w") as f:
            f.write(content)
