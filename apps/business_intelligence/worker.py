"""
Business Intelligence Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.business_intelligence.engine import BusinessIntelligenceEngine
from apps.business_intelligence.schemas import BusinessIntelligenceRequest


class BusinessIntelligenceWorker:
    """Thin adapter that exposes the BI engine to agents."""

    def __init__(self) -> None:
        self.engine = BusinessIntelligenceEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = BusinessIntelligenceRequest(**task)
        report = self.engine.analyze(request)
        return json.loads(report.model_dump_json())
