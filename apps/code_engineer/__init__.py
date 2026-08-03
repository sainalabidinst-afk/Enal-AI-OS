"""
Code Engineer
=============

Reference application #2: AI-powered code analysis and generation.
Full pipeline: Architecture Reader -> Dependency Graph -> Impact Analysis
-> Refactoring Suggestions -> Patch Generator -> Regression Risk -> Test Generator

Each component builds on the previous to provide a complete
code engineering workflow from analysis to safe deployment.
"""

import tempfile
from typing import Any

from apps.base import BaseReferenceApp


class CodeEngineerApp(BaseReferenceApp):
    name = "code-engineer"
    version = "1.0.0"
    description = "AI-powered code analysis, review, and generation with full pipeline"
    category = "software-engineering"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self):
        self._components_loaded = False
        self._repo_path: str | None = None

    async def _ensure_components(self):
        if self._components_loaded:
            return
        from apps.code_engineer.parser import code_parser
        from apps.code_engineer.analyzer import code_analyzer
        from apps.code_engineer.architecture_reader import ArchitectureReader, read_architecture
        from apps.code_engineer.dependency_graph import DependencyGraphBuilder
        from apps.code_engineer.impact_analyzer import ImpactAnalyzer
        from apps.code_engineer.refactoring_engine import RefactoringEngine
        from apps.code_engineer.patch_generator import PatchGenerator
        from apps.code_engineer.regression_analyzer import RegressionAnalyzer
        from apps.code_engineer.test_generator import TestGenerator
        from apps.code_engineer.architecture_patterns import architecture_pattern_analyzer, ArchitecturePatternAnalyzer
        from apps.code_engineer.secure_coding import secure_coding_analyzer, SecureCodingAnalyzer

        self.parser = code_parser
        self.analyzer = code_analyzer
        self.architecture_reader_cls = ArchitectureReader
        self.architecture_reader = read_architecture
        self.dependency_graph_builder = DependencyGraphBuilder
        self.impact_analyzer_cls = ImpactAnalyzer
        self.refactoring_engine_cls = RefactoringEngine
        self._repo_path = tempfile.mkdtemp()
        self.patch_generator_cls = lambda: PatchGenerator(self._repo_path)  # type: ignore[arg-type]
        self.regression_analyzer_cls = RegressionAnalyzer
        self.test_generator_cls = TestGenerator
        self.architecture_pattern_analyzer = architecture_pattern_analyzer
        self.secure_coding_analyzer = secure_coding_analyzer
        self._components_loaded = True

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        from backend.app.core.adaptive_runtime import adaptive_runtime

        context = context or {}
        project_id = context.get("project_id", "code-engineer-default")

        result = await adaptive_runtime.execute(
            user_input,
            project_id=project_id,
            force_pipeline=self.pipeline,
        )
        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "result": result,
        }

    async def analyze_repository(self, repo_path: str) -> dict[str, Any]:
        """Run full repository analysis pipeline."""
        await self._ensure_components()
        from pathlib import Path

        path = Path(repo_path)
        if not path.exists():
            return {"error": "Repository path not found: " + repo_path}

        self._repo_path = str(path)
        reader = self.architecture_reader_cls(str(path))
        architecture = await reader.read()
        if not architecture:
            return {"error": "Architecture analysis failed"}

        dep_builder = self.dependency_graph_builder(str(path))
        dep_graph_summary = await dep_builder.build()

        return {
            "app": self.name,
            "version": self.version,
            "architecture": architecture,
            "dependency_graph": {
                "total_modules": dep_graph_summary.total_modules,
                "total_dependencies": dep_graph_summary.total_dependencies,
                "circular_dependencies": len(dep_graph_summary.circular_dependencies),
                "orphan_modules": dep_graph_summary.orphan_modules,
            },
            "metadata": {
                "category": self.category,
                "capabilities_used": [
                    "architecture-analysis",
                    "dependency-analysis",
                    "code-analysis",
                    "refactoring",
                    "patch-generation",
                    "regression-analysis",
                    "test-generation",
                ],
            },
        }

    def parse_code(self, code: str, filename: str = "<unknown>") -> Any:
        """Parse Python code into AST."""
        import asyncio
        if not self._components_loaded:
            try:
                loop = asyncio.get_running_loop()
                loop.run_until_complete(self._ensure_components())
            except RuntimeError:
                asyncio.run(self._ensure_components())
        return self.parser.parse(code, filename=filename)

    def analyze_code(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        """Analyze Python code for issues, architecture patterns, and security."""
        import asyncio
        if not self._components_loaded:
            try:
                loop = asyncio.get_running_loop()
                loop.run_until_complete(self._ensure_components())
            except RuntimeError:
                asyncio.run(self._ensure_components())

        code_ast = self.parser.parse(code, filename=filename)
        issues = self.analyzer.analyze(code_ast)

        # Architecture pattern analysis
        arch_results = self.architecture_pattern_analyzer.analyze(code_ast)
        arch_findings = []
        for category, findings in arch_results.items():
            for finding in findings:
                arch_findings.append({
                    "category": f"architecture.{finding.category}",
                    "pattern": finding.pattern,
                    "severity": finding.severity,
                    "description": finding.description,
                    "recommendation": finding.recommendation,
                    "line": finding.line_number,
                    "confidence": finding.confidence,
                })

        # Secure coding analysis
        sec_results = self.secure_coding_analyzer.analyze(code_ast)
        sec_findings = []
        for category, findings in sec_results.items():
            for finding in findings:
                sec_findings.append({
                    "category": f"security.{finding.category}",
                    "pattern": finding.pattern,
                    "severity": finding.severity,
                    "description": finding.description,
                    "recommendation": finding.recommendation,
                    "line": finding.line_number,
                    "confidence": finding.confidence,
                })

        return {
            "filename": filename,
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

    async def analyze_code_async(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        """Async version of analyze_code."""
        await self._ensure_components()
        return self.analyze_code(code, filename)

    async def get_refactoring_suggestions(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        """Get refactoring suggestions for code."""
        await self._ensure_components()
        self.parser.parse(code, filename=filename)
        import os as _os, asyncio
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file = _os.path.join(tmpdir, filename)
            await asyncio.to_thread(self._write_file_sync, tmp_file, code)
            engine = self.refactoring_engine_cls(tmpdir)
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

    def _write_file_sync(self, path: str, content: str) -> None:
        """Synchronous file write helper."""
        with open(path, 'w') as f:
            f.write(content)

    async def generate_patch(self, original: str, modified: str, filename: str) -> dict[str, Any]:
        """Generate a rollback-ready patch between two versions."""
        await self._ensure_components()
        gen = self.patch_generator_cls()
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

    async def generate_tests(self, source_path: str, module_path: str) -> dict[str, Any]:
        """Generate tests for a Python module."""
        await self._ensure_components()
        gen = self.test_generator_cls()
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
        analyzer = self.regression_analyzer_cls()
        report = await analyzer.analyze_changes(
            repo_path=repo_path,
            changes=changes,
        )
        return report.to_dict()


def get_app() -> CodeEngineerApp:
    return CodeEngineerApp()
