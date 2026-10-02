"""
SRE Engineer Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.sre_engineer.engine import SREEngineerEngine
from apps.sre_engineer.schemas import SREEngineerRequest


class SREEngineerWorker:
    """Thin adapter that exposes the SRE Engineer engine to agents."""

    def __init__(self) -> None:
        self.engine = SREEngineerEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = SREEngineerRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["SREEngineerWorker"]
