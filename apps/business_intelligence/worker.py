"""
Business Intelligence Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.business_intelligence.engine import BusinessIntelligenceEngine
from apps.business_intelligence.schemas import BIRequest


class BusinessIntelligenceWorker:
    """Thin adapter that exposes the Business Intelligence engine to agents."""

    def __init__(self) -> None:
        self.engine = BusinessIntelligenceEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = BIRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["BusinessIntelligenceWorker"]
