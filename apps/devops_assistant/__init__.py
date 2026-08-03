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
from apps.devops_assistant.worker import DevOpsWorker


class DevOpsAssistantApp(BaseReferenceApp):
    name = "devops-assistant"
    version = "2.0.0"
    description = "CI/CD pipeline automation and infrastructure management"
    category = "devops"
    pipeline = ["perception", "memory", "planning", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DevOpsWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        return await self.worker.execute(user_input, context)


def get_app() -> DevOpsAssistantApp:
    return DevOpsAssistantApp()
