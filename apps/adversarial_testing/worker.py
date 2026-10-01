"""
Adversarial Testing Worker — thin adapter (per ADR-003).

Routes task requests to the Adversarial Testing Domain Engine.
"""

from __future__ import annotations

import uuid
from typing import Any

from apps.adversarial_testing.engine import AdversarialTestingEngine


class AdversarialTestingWorker:
    """
    Thin Worker adapter for the Adversarial Testing Capability Pack.

    Responsibilities:
        - Parse incoming task into test parameters
        - Delegate to AdversarialTestingEngine.test()
        - Return AdversarialTestResult as dict

    Usage::

        worker = AdversarialTestingWorker()
        result = await worker.execute(task)
    """

    def __init__(self, engine: AdversarialTestingEngine | None = None) -> None:
        self._engine = engine or AdversarialTestingEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute an adversarial testing task.

        Expected task format::

            {
                "subject": "The plan to test...",
                "subject_type": "plan",
                "context": "additional context",
                "evidence": {...},
                "constraints": ["..."],
                "attack_categories": ["external_shock", ...],
                "attack_budget": 10,
                "existing_hardening": ["..."],
            }

        Returns:
            AdversarialTestResult as a JSON-serializable dict.
        """
        result = self._engine.test(
            subject=task.get("subject", ""),
            subject_type=task.get("subject_type", "plan"),
            context=task.get("context"),
            evidence=task.get("evidence"),
            constraints=task.get("constraints"),
            attack_categories=task.get("attack_categories"),
            attack_budget=task.get("attack_budget", 10),
            existing_hardening=task.get("existing_hardening"),
        )

        # Set request_id
        result.request_id = task.get("request_id", str(uuid.uuid4()))

        return result.to_dict()
