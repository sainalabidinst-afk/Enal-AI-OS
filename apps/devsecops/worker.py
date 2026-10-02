"""
DevSecOps Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.devsecops.engine import DevSecOpsEngine
from apps.devsecops.schemas import DevSecOpsRequest


class DevSecOpsWorker:
    """Thin adapter that exposes the DevSecOps engine to agents."""

    def __init__(self) -> None:
        self.engine = DevSecOpsEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = DevSecOpsRequest(**task)
        report = self.engine.analyze(request)
        return json.loads(report.model_dump_json())
