"""
UI/UX Designer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.ui_ux_designer.engine import UIUXDesignerEngine
from apps.ui_ux_designer.worker import UIUXDesignerWorker
from apps.ui_ux_designer.schemas import (
    UIUXDesignerRequest,
    UIUXDesignerReport,
    OperationType,
    Priority,
    OutputFormat,
    BusinessContext,
    StakeholderInput,
    Persona,
    QualityAttributes,
    UXResearchResult,
    DesignSystem,
    DesignToken,
    ComponentSpec,
    Prototype,
    PrototypeScreen,
    AccessibilityReport,
    AccessibilityViolation,
    UXDesignRecord,
)


class UIUXDesignerApp(BaseReferenceApp):
    name = "ui-ux-designer"
    version = "1.0.0"
    description = "User experience research, design systems, and accessibility"
    category = "design"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = UIUXDesignerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> UIUXDesignerApp:
    return UIUXDesignerApp()

__all__ = [
    "UIUXDesignerApp",
    "get_app",
    "UIUXDesignerEngine",
    "UIUXDesignerWorker",
    "UIUXDesignerRequest",
    "UIUXDesignerReport",
    "OperationType",
    "Priority",
    "OutputFormat",
    "BusinessContext",
    "StakeholderInput",
    "Persona",
    "QualityAttributes",
    "UXResearchResult",
    "DesignSystem",
    "DesignToken",
    "ComponentSpec",
    "Prototype",
    "PrototypeScreen",
    "AccessibilityReport",
    "AccessibilityViolation",
    "UXDesignRecord",
]
