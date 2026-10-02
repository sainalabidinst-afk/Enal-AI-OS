"""
Observability Capability Pack — Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.observability.engine import ObservabilityAnalystEngine
from apps.observability.schemas import ObservabilityAnalystRequest


class ObservabilityWorker:
    """Thin adapter that exposes the Observability engine to agents."""

    def __init__(self) -> None:
        self.engine = ObservabilityAnalystEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = ObservabilityAnalystRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["ObservabilityWorker"]
