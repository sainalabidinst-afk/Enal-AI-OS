"""
Documentation Engineer Reference App
========================================

Demonstrates ECP capabilities for automated technical documentation generation
and validation.

Workflow:
User Request
    ↓
Intent Router
    ↓
Capability Graph → documentation-*
    ↓
Task Planner
    ↓
Subtasks:
- OpenAPI Generation
- SDK Documentation
- Architecture Documentation
- Documentation Validation
- Release Notes Generation
    ↓
Execution Planner
    ↓
Execution Runtime
    ↓
Documentation Worker
    ↓
Documentation Engine
    ↓
Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.documentation_engineer.worker import DocumentationWorker


class DocumentationEngineerApp(BaseReferenceApp):
    name = "documentation-engineer"
    version = "1.0.0"
    description = "Automated technical documentation generation and validation"
    category = "documentation"
    pipeline = ["perception", "memory", "planning", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DocumentationWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        return await self.worker.execute(user_input, context)


def get_app() -> DocumentationEngineerApp:
    return DocumentationEngineerApp()
