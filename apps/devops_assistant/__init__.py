"""
DevOps Assistant Reference App
====================================

Demonstrates ECP capabilities for CI/CD and infrastructure automation.

Workflow:
User Request
    ↓
Intent Router
    ↓
Capability Graph → devops-*
    ↓
Task Planner
    ↓
Subtasks:
- Infrastructure Design
- CI/CD Pipeline
- Monitoring Setup
- Deployment
    ↓
Execution Planner
    ↓
Execution Runtime
    ↓
DevOps Worker
    ↓
DevOps Engine
    ↓
Result
"""

from typing import Any
from apps.base import BaseReferenceApp
from apps.devops_assistant.engine import devops_engine


class DevOpsAssistantApp(BaseReferenceApp):
    name = "devops-assistant"
    version = "1.0.0"
    description = "CI/CD pipeline automation and infrastructure management"
    category = "devops"
    pipeline = ["perception", "memory", "planning", "reasoning", "decision", "action"]

    def __init__(self):
        self.engine = devops_engine

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        project_id = context.get("project_id", "devops-assistant-default")

        pipeline = await self.engine.generate_pipeline(project_id)
        infra = await self.engine.design_infrastructure(project_id)
        deployment = await self.engine.plan_deployment(project_id)

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": {
                "pipeline": pipeline,
                "infrastructure": infra,
                "deployment": deployment,
            },
            "metadata": {
                "category": self.category,
                "capabilities_used": [
                    "infrastructure-design",
                    "ci-cd",
                    "monitoring",
                    "deployment",
                ],
            },
        }


def get_app() -> DevOpsAssistantApp:
    return DevOpsAssistantApp()
