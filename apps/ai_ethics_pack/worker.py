"""
AI Ethics & Governance Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.ai_ethics_pack.engine import AIEthicsEngine
from apps.ai_ethics_pack.schemas import AIEthicsGovernanceRequest


class AIEthicsGovernanceWorker:
    """Thin adapter that exposes the AI Ethics engine to agents."""

    def __init__(self) -> None:
        self.engine = AIEthicsEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = AIEthicsGovernanceRequest(**task)
        report = self.engine.analyze(request)
        return json.loads(report.model_dump_json())
