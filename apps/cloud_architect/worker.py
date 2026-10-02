"""
Cloud Architect Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.cloud_architect.engine import CloudArchitectEngine
from apps.cloud_architect.schemas import CloudArchitectRequest


class CloudArchitectWorker:
    """Thin adapter that exposes the Cloud Architect engine to agents."""

    def __init__(self) -> None:
        self.engine = CloudArchitectEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = CloudArchitectRequest(**task)
        report = self.engine.design(request)
        return json.loads(report.model_dump_json())


__all__ = ["CloudArchitectWorker"]
