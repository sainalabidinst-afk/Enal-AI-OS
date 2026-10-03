"""
AI Ethics & Governance Capability Pack — __init__.py
"""

from typing import Any

from apps.ai_ethics_pack.engine import AIEthicsGovernanceEngine
from apps.ai_ethics_pack.schemas import (
    AIEthicsGovernanceReport,
    AIEthicsGovernanceRequest,
    AIEthicsInputs,
    AIEthicsOperation,
    AIEthicsRecord,
    BiasFinding,
    ComplianceMapping,
    EthicsAssessment,
    FairnessMetric,
)
from apps.ai_ethics_pack.worker import AIEthicsGovernanceWorker
from apps.base import BaseReferenceApp


class AIEthicsGovernanceApp(BaseReferenceApp):
    name = "ai-ethics-governance"
    version = "2.5.0"
    description = (
        "Fairness auditing, bias detection, explainability analysis, "
        "and regulatory compliance for AI systems"
    )
    category = "governance"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = AIEthicsGovernanceWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> AIEthicsGovernanceApp:
    return AIEthicsGovernanceApp()


__all__ = [
    "AIEthicsGovernanceApp",
    "get_app",
    "AIEthicsGovernanceEngine",
    "AIEthicsGovernanceWorker",
    "AIEthicsGovernanceRequest",
    "AIEthicsGovernanceReport",
    "AIEthicsOperation",
    "AIEthicsInputs",
    "AIEthicsRecord",
    "BiasFinding",
    "FairnessMetric",
    "EthicsAssessment",
    "ComplianceMapping",
]
