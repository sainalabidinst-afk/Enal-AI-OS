"""
HSE Specialist Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.hse_specialist.engine import HSESpecialistEngine
from apps.hse_specialist.schemas import HSESpecialistRequest


class HSESpecialistWorker:
    """Thin adapter that exposes the HSE Specialist engine to agents."""

    def __init__(self) -> None:
        self.engine = HSESpecialistEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = HSESpecialistRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["HSESpecialistWorker"]
