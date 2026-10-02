"""
Supply Chain Analyst Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.supply_chain_analyst.engine import SupplyChainEngine
from apps.supply_chain_analyst.schemas import SupplyChainRequest


class SupplyChainWorker:
    """Thin adapter that exposes the Supply Chain engine to agents."""

    def __init__(self) -> None:
        self.engine = SupplyChainEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = SupplyChainRequest(**task)
        report = self.engine.analyze(request)
        return json.loads(report.model_dump_json())
