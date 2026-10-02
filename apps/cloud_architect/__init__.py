"""
Cloud Architect — __init__.py
"""

from typing import Any

from apps.cloud_architect.engine import CloudArchitectEngine
from apps.cloud_architect.schemas import (
    ArchitecturePattern,
    BusinessContext,
    CloudArchitectRecord,
    CloudArchitectReport,
    CloudArchitectRequest,
    CloudProvider,
    CostOptimizationStrategy,
    LandingZoneSpec,
    RegionStrategy,
)
from apps.cloud_architect.worker import CloudArchitectWorker
from apps.base import BaseReferenceApp


class CloudArchitectApp(BaseReferenceApp):
    name = "cloud-architect"
    version = "1.0.0"
    description = "Cloud architecture design, multi-region strategy, cost optimization, and DR planning"
    category = "infrastructure"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = CloudArchitectWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> CloudArchitectApp:
    return CloudArchitectApp()


__all__ = [
    "CloudArchitectApp",
    "get_app",
    "CloudArchitectEngine",
    "CloudArchitectWorker",
    "CloudArchitectRequest",
    "CloudArchitectReport",
    "CloudProvider",
    "ArchitecturePattern",
    "RegionStrategy",
    "CostOptimizationStrategy",
    "BusinessContext",
    "LandingZoneSpec",
    "CloudArchitectRecord",
]
