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
    version = "2.1.0"
    description = "Autonomous self-improvement, ECP meta-analysis, and personal growth engine"
    category = "self-development"
    pipeline = ["perception", "memory", "analysis", "proposal", "validation", "approval", "action"]

    def __init__(self):
        self.engine = self_development_engine

    GROWTH_KEYWORDS = (
        "progres",
        "progress",
        "analitik",
        "analytics",
        "rekomendas",
        "recommend",
        "kebiasaan",
        "habit",
        "streak",
        "check-in",
        "check in",
        "goal",
        "tujuan",
        "belajar",
        "learn",
        "growth",
    )

    def is_growth_request(self, user_input: str) -> bool:
        """Detect whether the request targets the personal growth engine."""
        lowered = user_input.lower()
        return any(keyword in lowered for keyword in self.GROWTH_KEYWORDS)

    async def growth_report(self, user_input: str) -> dict[str, Any]:
        """Return progress, goals, habits, and next-step recommendations."""
        progress = await self.engine.get_progress()
        goals = await self.engine.list_goals()
        habits = await self.engine.habit_statuses()
        recommendations = await self.engine.recommend_next()
        return {
            "mode": "growth_engine",
            "input": user_input,
            "progress": progress,
            "goals": goals,
            "habits": habits,
            "recommendations": recommendations,
        }

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        context.get("project_id", "self-development-default")

        lowered = user_input.lower()
        if "ecp" in lowered or "platform" in lowered or "core" in lowered:
            ecp_analysis = await self.engine.analyze_ecp()
            proposals = await self.engine.propose_capabilities()
            improvements = await self.engine.propose_improvements()
            return {
                "app": self.name,
                "version": self.version,
                "input": user_input,
                "pipeline": self.pipeline,
                "result": {
                    "mode": "ecp_meta_analysis",
                    "ecp_analysis": ecp_analysis,
                    "capability_proposals": proposals,
                    "improvement_proposals": improvements,
                    "requires_approval": True,
                },
                "metadata": {
                    "category": self.category,
                    "capabilities_used": [
                        "platform-analysis",
                        "capability-proposal",
                        "cross-pack-learning",
                        "governance",
                        "approval-management",
                    ],
                },
            }

        if self.is_growth_request(lowered):
            report = await self.growth_report(user_input)
            return {
                "app": self.name,
                "version": self.version,
                "input": user_input,
                "pipeline": self.pipeline,
                "result": report,
                "metadata": {
                    "category": self.category,
                    "capabilities_used": [
                        "learning-analytics",
                        "goal-alignment",
                        "recommendation-engine",
                        "habit-tracking",
                        "cross-pack-integration",
                    ],
                },
            }

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


__all__ = ["SelfDevelopmentApp", "get_app"]
