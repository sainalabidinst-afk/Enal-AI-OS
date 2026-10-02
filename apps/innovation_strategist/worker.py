"""
Innovation Strategist Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.innovation_strategist.engine import InnovationStrategistEngine
from apps.innovation_strategist.schemas import InnovationStrategistRequest


class InnovationStrategistWorker:
    """Thin adapter that exposes the Innovation Strategist engine to agents."""

    def __init__(self) -> None:
        self.engine = InnovationStrategistEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = InnovationStrategistRequest(**task)
        report = self.engine.analyze(request)
        return json.loads(report.model_dump_json())
