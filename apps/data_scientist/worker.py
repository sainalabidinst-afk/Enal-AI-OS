"""
Data Scientist Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.data_scientist.engine import DataScientistEngine
from apps.data_scientist.schemas import DataScienceRequest


class DataScientistWorker:
    """Thin adapter that exposes the Data Scientist engine to agents."""

    def __init__(self) -> None:
        self.engine = DataScientistEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = DataScienceRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["DataScientistWorker"]
