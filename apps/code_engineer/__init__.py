"""
Code Engineer
=============

Reference application #2: AI-powered code analysis and generation.
Full pipeline: Architecture Reader → Dependency Graph → Impact Analysis
→ Refactoring Suggestions → Patch Generator → Regression Risk → Test Generator

Each component builds on the previous to provide a complete
code engineering workflow from analysis to safe deployment.
"""

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

    async def _ensure_components(self):
        if self._components_loaded:
            return
        from apps.code_engineer.parser import code_parser
        from apps.code_engineer.analyzer import code_analyzer
        from apps.code_engineer.architecture_reader import architecture_reader
        from apps.code_engineer.dependency_graph import DependencyGraphBuilder
        from apps.code_engineer.impact_analyzer import ImpactAnalyzer
        from apps.code_engineer.refactoring_engine import refactoring_engine
        from apps.code_engineer.patch_generator import patch_generator
        from apps.code_engineer.regression_analyzer import regression_analyzer
        from apps.code_engineer.test_generator import test_generator

        self.parser = code_parser
        self.analyzer = code_analyzer
        self.architecture_reader = architecture_reader
        self.dependency_graph_builder = DependencyGraphBuilder
        self.impact_analyzer_cls = ImpactAnalyzer
        self.refactoring_engine = refactoring_engine
        self.patch_generator = patch_generator
        self.regression_analyzer = regression_analyzer
        self.test_generator = test_generator
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
            return {"error": f"Repository path not found: {repo_path}"}

        # Step 1: Architecture Reader
        architecture = await self.architecture_reader.analyze(str(path))
        if not architecture:
            return {"error": "Architecture analysis failed"}

        # Step 2: Dependency Graph
        dep_graph_cls = self.dependency_graph_builder(str(path))
        dep_graph_summary = await dep_graph_cls.build()

        # Step 3: Impact analysis (baseline)
        impact_cls = self.impact_analyzer_cls(str(path))

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
        try:
            loop = asyncio.get_running_loop()
            if not self._components_loaded:
                loop.run_until_complete(self._ensure_components())
        except RuntimeError:
            pass
        return self.parser.parse(code, filename=filename)

    def analyze_code(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        """Analyze Python code for issues."""
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            if not self._components_loaded:
                loop.run_until_complete(self._ensure_components())
        except RuntimeError:
            pass

        code_ast = self.parser.parse(code, filename=filename)
        issues = self.analyzer.analyze(code_ast)
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
        }

    async def analyze_code_async(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        """Async version of analyze_code."""
        await self._ensure_components()
        return self.analyze_code(code, filename)

    async def get_refactoring_suggestions(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        """Get refactoring suggestions for code."""
        await self._ensure_components()
        code_ast = self.parser.parse(code, filename=filename)
        suggestions = await self.refactoring_engine.analyze(code_ast)
        return {
            "filename": filename,
            "suggestions": [
                {
                    "severity": s.severity,
                    "category": s.category,
                    "description": s.description,
                    "recommendation": s.recommendation,
                    "line": s.line_number,
                    "confidence": s.confidence,
                }
                for s in suggestions
            ],
        }

    async def generate_patch(self, original: str, modified: str, filename: str) -> dict[str, Any]:
        """Generate a rollback-ready patch between two versions."""
        await self._ensure_components()
        patches = await self.patch_generator.generate_patches(
            {filename: (original, modified)}
        )
        if patches:
            patch = patches[0]
            return {
                "filename": filename,
                "patch_id": patch.patch_id,
                "diff": patch.diff,
                "diff_type": patch.diff_type,
                "is_valid": await self.patch_generator.validate_patch(patch),
            }
        return {"error": "No patches generated"}

    async def generate_tests(self, source_path: str, module_path: str) -> dict[str, Any]:
        """Generate tests for a Python module."""
        await self._ensure_components()
        test_file = await self.test_generator.generate_for_module(
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
        report = await self.regression_analyzer.analyze_changes(
            repo_path=repo_path,
            changes=changes,
        )
        return report.to_dict()


def get_app() -> CodeEngineerApp:
    return CodeEngineerApp()
