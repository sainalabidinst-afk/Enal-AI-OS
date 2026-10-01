"""
Adversarial Testing — Self-Correction & Adversarial Testing Agent ("Devil's Advocate").

Capability Pack that generates adversarial attack scenarios to find
weaknesses in plans, strategies, and recommendations. Forces hardening
through a pass/fail gate before results are considered production-ready.

Pipeline:
    AdversarialTestRequest
        ↓
    Attack Vector Generator (generate diverse worst-case scenarios)
        ↓
    Assumption Auditor (identify hidden assumptions)
        ↓
    Vulnerability Scanner (score and assess exploitability)
        ↓
    Hardening Advisor (recommend mitigations)
        ↓
    Adversarial Gate (pass/fail evaluation)
        ↓
    Explanation Generator (full reasoning chain)
        ↓
    AdversarialTestResult
"""

from typing import Any

from apps.adversarial_testing.engine import AdversarialTestingEngine
from apps.adversarial_testing.schemas import (
    AdversarialTestResult,
    AttackCategory,
    AttackRequest,
    AttackVector,
    GateResult,
    HardeningAction,
    Priority,
    Severity,
    SubjectType,
    Vulnerability,
)
from apps.adversarial_testing.worker import AdversarialTestingWorker
from apps.base import BaseReferenceApp


class AdversarialTestingApp(BaseReferenceApp):
    name = "adversarial-testing"
    version = "1.0.0"
    description = "Adversarial testing agent that attacks plans to ensure anti-fragility"
    category = "testing"
    pipeline = ["perception", "memory", "reasoning", "simulation", "decision"]

    def __init__(self) -> None:
        self.worker = AdversarialTestingWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("subject", user_input)
        return await self.worker.execute(task)


def get_app() -> AdversarialTestingApp:
    return AdversarialTestingApp()


__all__ = [
    "AdversarialTestingApp",
    "get_app",
    "AdversarialTestingEngine",
    "AdversarialTestingWorker",
    "AdversarialTestResult",
    "AttackVector",
    "AttackRequest",
    "AttackCategory",
    "SubjectType",
    "Severity",
    "Priority",
    "Vulnerability",
    "HardeningAction",
    "GateResult",
]
