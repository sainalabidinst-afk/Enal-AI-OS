"""
Observability Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.observability.engine import ObservabilityAnalystEngine
from apps.observability.schemas import (
    AnomalyFinding,
    AnomalyReport,
    BusinessContext,
    LogEntry,
    LogPattern,
    MetricSample,
    MetricSummary,
    ObservabilityAnalystRequest,
    ObservabilityInputs,
    ObservabilityOperation,
    ObservabilityRecord,
    ObservabilityReport,
    TraceSpan,
    TraceSummary,
)
from apps.observability.worker import ObservabilityWorker


class ObservabilityApp(BaseReferenceApp):
    name = "observability"
    version = "2.3.0"
    description = (
        "Metrics collection, distributed tracing, log analysis, and anomaly "
        "detection for platform observability"
    )
    category = "platform"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = ObservabilityWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> ObservabilityApp:
    return ObservabilityApp()


__all__ = [
    "ObservabilityApp",
    "get_app",
    "ObservabilityAnalystEngine",
    "ObservabilityWorker",
    "ObservabilityAnalystRequest",
    "ObservabilityReport",
    "ObservabilityOperation",
    "ObservabilityInputs",
    "MetricSummary",
    "TraceSummary",
    "LogPattern",
    "AnomalyReport",
    "AnomalyFinding",
    "BusinessContext",
    "MetricSample",
    "LogEntry",
    "TraceSpan",
    "ObservabilityRecord",
]
