"""
AI Ethics & Governance Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.ai_ethics_pack.engine import AIEthicsGovernanceEngine
from apps.ai_ethics_pack.schemas import EthicsRequest


class AIEthicsGovernanceWorker:
    """Thin adapter that exposes the AI Ethics engine to agents."""

    def __init__(self) -> None:
        self.engine = AIEthicsGovernanceEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = EthicsRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["AIEthicsGovernanceWorker"]
