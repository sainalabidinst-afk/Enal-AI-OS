"""
Cybersecurity Analyst Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.cybersecurity_analyst.engine import CybersecurityAnalystEngine
from apps.cybersecurity_analyst.schemas import CybersecurityRequest


class CybersecurityAnalystWorker:
    """Thin adapter that exposes the Cybersecurity Analyst engine to agents."""

    def __init__(self) -> None:
        self.engine = CybersecurityAnalystEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = CybersecurityRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["CybersecurityAnalystWorker"]
