"""
Documentation Worker
====================

Execution adapter bridging the reference app and the upgraded engine.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.documentation_engineer.engine import DocumentationEngine
from apps.documentation_engineer.schemas import (
    DocumentationRequest,
    OperationType,
    DocumentationTarget,
    GenerationOptions,
    DocumentationInput,
)

logger = logging.getLogger(__name__)


class DocumentationWorker:
    """Execution adapter for Documentation Engineer."""

    def __init__(self) -> None:
        self._engine = DocumentationEngine()

    async def execute(self, user_input: str, context: dict[str, Any]) -> dict[str, Any]:
        target_data = context.get("target", {})
        target = DocumentationTarget(**target_data)

        options_data = context.get("options", {})
        options = GenerationOptions(**options_data)

        inputs_data = context.get("inputs", {})
        inputs = DocumentationInput(**inputs_data)

        op_value = context.get("operation", "openapi_generation")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.openapi_generation

        request = DocumentationRequest(
            operation=operation,
            target=target,
            options=options,
            inputs=inputs,
        )

        report = self._engine.generate(request)
        return {
            "app": "documentation-engineer",
            "input": user_input,
            "result": report.to_dict(),
            "metadata": {
                "capabilities_used": [
                    "openapi",
                    "sdk-docs",
                    "architecture-docs",
                    "validation",
                    "release-notes",
                ],
            },
        }
