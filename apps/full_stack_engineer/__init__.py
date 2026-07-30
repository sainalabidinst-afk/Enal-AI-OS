"""
Full Stack Engineer
====================

Capability pack covering:
- F1 Architecture Review
- F2 Code Review
- F3 Refactoring Planner
- F4 Test Engineer
- F5 Performance Engineer
- F6 Release Engineer

Built on top of the existing code-engineer primitives:
Architecture Reader -> Dependency Graph -> Impact Analysis
-> Refactoring Suggestions -> Patch Generator -> Regression Risk -> Test Generator
"""

from typing import Any

from apps.base import BaseReferenceApp


class FullStackEngineerApp(BaseReferenceApp):
    name = "full-stack-engineer"
    version = "1.0.0"
    description = "Full-stack engineering: architecture review, code review, refactoring, testing, performance, and release engineering."
    category = "software-engineering"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self):
        self._components_loaded = False

    async def _ensure_components(self):
        if self._components_loaded:
            return
        from apps.code_engineer.architecture_reader import ArchitectureReader, read_architecture
        from apps.code_engineer.dependency_graph import DependencyGraphBuilder
        from apps.code_engineer.impact_analyzer import ImpactAnalyzer
        from apps.code_engineer.refactoring_engine import RefactoringEngine
        from apps.code_engineer.regression_analyzer import RegressionAnalyzer
        from apps.code_engineer.test_generator import TestGenerator
        from apps.full_stack_engineer.architecture_review import ArchitectureReviewEngine
        from apps.full_stack_engineer.code_review import FullStackCodeReviewEngine
        from apps.full_stack_engineer.performance_engineer import PerformanceEngineer
        from apps.full_stack_engineer.refactoring_planner import RefactoringPlanner
        from apps.full_stack_engineer.release_engineer import ReleaseEngineer
        from apps.full_stack_engineer.test_engineer import TestEngineer

        self.architecture_review_engine_cls = ArchitectureReviewEngine
        self.code_review_engine_cls = FullStackCodeReviewEngine
        self.refactoring_planner_cls = RefactoringPlanner
        self.test_engineer_cls = TestEngineer
        self.performance_engineer_cls = PerformanceEngineer
        self.release_engineer_cls = ReleaseEngineer
        self._components_loaded = True

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        from backend.app.core.adaptive_runtime import adaptive_runtime

        context = context or {}
        project_id = context.get("project_id", "full-stack-engineer-default")
        result = await adaptive_runtime.execute(
            user_input,
            project_id=project_id,
            force_pipeline=self.pipeline,
        )
        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": result,
            "metadata": {
                "category": self.category,
            },
        }

    async def review_architecture(self, repo_path: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        await self._ensure_components()
        engine = self.architecture_review_engine_cls()
        return await engine.review(repo_path, context)

    async def review_code(self, code: str, filename: str = "<unknown>", context: dict[str, Any] | None = None) -> dict[str, Any]:
        await self._ensure_components()
        engine = self.code_review_engine_cls()
        return await engine.review(code, filename, context)

    async def plan_refactoring(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        await self._ensure_components()
        engine = self.refactoring_planner_cls()
        return await engine.plan(code, filename)

    async def engineer_tests(self, source_path: str, module_path: str) -> dict[str, Any]:
        await self._ensure_components()
        engine = self.test_engineer_cls()
        return await engine.engineer(source_path, module_path)

    async def analyze_performance(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        await self._ensure_components()
        engine = self.performance_engineer_cls()
        return await engine.analyze(code, filename)

    async def review_release(self, changes: list[dict[str, Any]], context: dict[str, Any] | None = None) -> dict[str, Any]:
        await self._ensure_components()
        engine = self.release_engineer_cls()
        return await engine.review(changes, context)


def get_app() -> FullStackEngineerApp:
    return FullStackEngineerApp()