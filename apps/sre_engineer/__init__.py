"""
SRE Engineer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.sre_engineer.engine import SREEngineerEngine
from apps.sre_engineer.schemas import (
    BusinessContext,
    DashboardSpec,
    IncidentSeverity,
    MonitoringStack,
    RunbookSpec,
    ServiceLevelIndicator,
    SLOSpec,
    SREConfig,
    SREEngineerRecord,
    SREEngineerReport,
    SREEngineerRequest,
    SREOperation,
)
from apps.sre_engineer.worker import SREEngineerWorker


class SREEngineerApp(BaseReferenceApp):
    name = "sre-engineer"
    version = "1.0.0"
    description = "Site reliability engineering, observability, SLOs, and incident response"
    category = "infrastructure"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = SREEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> SREEngineerApp:
    return SREEngineerApp()


__all__ = [
    "SREEngineerApp",
    "get_app",
    "SREEngineerEngine",
    "SREEngineerWorker",
    "SREEngineerRequest",
    "SREEngineerReport",
    "SREOperation",
    "MonitoringStack",
    "ServiceLevelIndicator",
    "SLOSpec",
    "DashboardSpec",
    "RunbookSpec",
    "IncidentSeverity",
    "SREConfig",
    "BusinessContext",
    "SREEngineerRecord",
]
