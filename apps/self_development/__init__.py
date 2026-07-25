"""
Self Development Reference App
====================================

Demonstrates ECP capabilities for autonomous self-improvement.

Workflow:
User Request
    ↓
Intent Router
    ↓
Capability Graph → self-development
    ↓
Task Planner
    ↓
Subtasks:
- Analyze Project
- Identify Problems
- Propose Solution
- Generate Patch
- Run Tests
- Await Approval
- Apply Changes
    ↓
Execution Planner
    ↓
Execution Runtime
    ↓
Self Development Worker
    ↓
Self Development Engine
    ↓
Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.self_development.engine import self_development_engine


class SelfDevelopmentApp(BaseReferenceApp):
    name = "self-development"
    version = "1.0.0"
    description = "Autonomous self-improvement with user approval"
    category = "self-development"
    pipeline = ["perception", "memory", "analysis", "proposal", "validation", "approval", "action"]

    def __init__(self):
        self.engine = self_development_engine

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        context.get("project_id", "self-development-default")

        project_analysis = await self.engine.analyze_project()
        problems = await self.engine.identify_problems()
        solutions = []
        patches = []
        for problem in problems:
            problem_id = problem.get("id", "")
            solution = await self.engine.propose_solution(problem_id)
            patch = await self.engine.generate_patch(problem_id)
            await self.engine.get_approval_status(problem_id)
            solutions.append(solution)
            patches.append(patch)

        tests_result = await self.engine.run_tests()

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": {
                "project_analysis": project_analysis,
                "problems": problems,
                "solutions": solutions,
                "patches": patches,
                "tests": tests_result,
                "requires_approval": True,
            },
            "metadata": {
                "category": self.category,
                "capabilities_used": [
                    "architecture-analysis",
                    "code-review",
                    "testing",
                    "documentation",
                    "approval-management",
                ],
            },
        }


def get_app() -> SelfDevelopmentApp:
    return SelfDevelopmentApp()
