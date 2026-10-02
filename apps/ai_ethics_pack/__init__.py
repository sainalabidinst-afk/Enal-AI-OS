"""
AI Ethics & Governance Pack
============================

Demonstrates ECP capabilities for AI ethics assessment and governance.

Workflow:
    User Request
        ↓
    Intent Router
        ↓
    Capability Graph → ai-ethics-governance-*
        ↓
    Task Planner
        ↓
    Subtasks:
    - Fairness Assessment
    - Bias Detection
    - Risk Assessment
    - Recommendation Generation
        ↓
    Execution Planner
        ↓
    Execution Runtime
        ↓
    Ethics Worker
        ↓
    Ethics Assessment Engine (full governance pipeline)
        ↓
    Result
"""

from typing import Any

from apps.ai_ethics_pack.engine import AIEthicsGovernanceEngine
from apps.ai_ethics_pack.schemas import (
    BiasFinding,
    BiasMetric,
    BusinessContext,
    EthicsConfig,
    EthicsFramework,
    EthicsOperation,
    EthicsPackRecord,
    EthicsReport,
    EthicsRequest,
    EthicsRisk,
    FairnessViolation,
    ProtectedAttribute,
    Severity,
)
from apps.ai_ethics_pack.worker import AIEthicsGovernanceWorker
from apps.base import BaseReferenceApp


class AIEthicsGovernanceApp(BaseReferenceApp):
    name = "ai-ethics-governance"
    version = "1.0.0"
    description = "AI ethics assessment and governance: bias detection, fairness auditing, explainability, and impact analysis"  # noqa: E501
    category = "ethics"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = AIEthicsGovernanceWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> AIEthicsGovernanceApp:
    return AIEthicsGovernanceApp()


__all__ = [
    "AIEthicsGovernanceApp",
    "AIEthicsGovernanceEngine",
    "AIEthicsGovernanceWorker",
    "EthicsFramework",
    "EthicsOperation",
    "BiasMetric",
    "Severity",
    "ProtectedAttribute",
    "BusinessContext",
    "EthicsConfig",
    "EthicsRequest",
    "BiasFinding",
    "FairnessViolation",
    "EthicsRisk",
    "EthicsReport",
    "EthicsPackRecord",
]
