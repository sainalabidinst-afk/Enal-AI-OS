"""
Product Worker
==============

Execution adapter bridging the reference app and the upgraded engine.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.product_manager.engine import ProductManagerEngine
from apps.product_manager.schemas import (
    ProductManagementRequest,
    OperationType,
    ProductContext,
    BacklogInput,
    RoadmapInput,
    OKRInput,
    Constraints,
    PrioritizationOptions,
)

logger = logging.getLogger(__name__)


class ProductWorker:
    """Execution adapter for Product Manager."""

    def __init__(self) -> None:
        self._engine = ProductManagerEngine()

    async def execute(self, user_input: str, context: dict[str, Any]) -> dict[str, Any]:
        ctx_data = context.get("product_context", {})
        product_context = ProductContext(**ctx_data)

        inputs_data = context.get("inputs", {})
        backlog_items = inputs_data.get("backlog_items", [])
        roadmap_items = inputs_data.get("roadmap_items", [])
        okrs = inputs_data.get("okrs", [])
        backlog_input = BacklogInput(items=backlog_items)
        roadmap_input = RoadmapInput(items=roadmap_items)
        okr_input = OKRInput(objectives=okrs)

        constraints_data = context.get("constraints", {})
        constraints = Constraints(**constraints_data)

        options_data = context.get("options", {})
        options = PrioritizationOptions(**options_data)

        op_value = context.get("operation", "backlog_management")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.backlog_management

        request = ProductManagementRequest(
            operation=operation,
            product_context=product_context,
            inputs={},
            constraints=constraints,
            options=options,
        )
        request.inputs.backlog = backlog_input
        request.inputs.roadmap = roadmap_input
        request.inputs.okrs = okr_input

        report = self._engine.manage(request)
        return {
            "app": "product-manager",
            "input": user_input,
            "result": report.to_dict(),
            "metadata": {
                "capabilities_used": [
                    "roadmap",
                    "backlog",
                    "sprint",
                    "okr",
                    "prioritization",
                    "release",
                ],
            },
        }
