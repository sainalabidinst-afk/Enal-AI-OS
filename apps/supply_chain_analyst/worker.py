"""
Supply Chain Analyst Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.supply_chain_analyst.engine import SupplyChainAnalystEngine
from apps.supply_chain_analyst.schemas import SupplyChainRequest


class SupplyChainAnalystWorker:
    """Thin adapter that exposes the Supply Chain Analyst engine to agents."""

    def __init__(self) -> None:
        self.engine = SupplyChainAnalystEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = SupplyChainRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["SupplyChainAnalystWorker"]
