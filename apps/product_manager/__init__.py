"""
Product Manager Reference App
===============================

Demonstrates ECP capabilities for product management, roadmap planning,
backlog management, sprint planning, OKR/KPI tracking, and prioritization.

Workflow:
User Request
    ↓
Intent Router
    ↓
Capability Graph → product-*
    ↓
Task Planner
    ↓
Subtasks:
- Roadmap Management
- Backlog Management
- Sprint Planning
- OKR/KPI Tracking
- Prioritization
- Release Coordination
    ↓
Execution Planner
    ↓
Execution Runtime
    ↓
Product Worker
    ↓
Product Engine
    ↓
Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.product_manager.worker import ProductWorker


class ProductManagerApp(BaseReferenceApp):
    name = "product-manager"
    version = "1.0.0"
    description = "Product management, roadmap planning, and prioritization"
    category = "product"
    pipeline = ["perception", "memory", "planning", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = ProductWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        return await self.worker.execute(user_input, context)


def get_app() -> ProductManagerApp:
    return ProductManagerApp()
