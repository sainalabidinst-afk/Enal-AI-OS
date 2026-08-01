"""
Decision Intelligence Worker — thin adapter (per ADR-003).

Routes task requests to the Decision Intelligence Domain Engine.
Does not own business logic; delegates to DecisionIntelligenceEngine.
"""

from __future__ import annotations

from typing import Any

from apps.decision_intelligence.engine import DecisionIntelligenceEngine
from apps.decision_intelligence.schemas import DecisionRequest


class DecisionIntelligenceWorker:
    """
    Thin Worker adapter for the Decision Intelligence Capability Pack.

    Responsibilities:
        - Parse incoming task into DecisionRequest
        - Delegate to DecisionIntelligenceEngine.evaluate()
        - Return DecisionResult as dict

    Usage::

        worker = DecisionIntelligenceWorker()
        result = await worker.execute(task)
    """

    def __init__(self, engine: DecisionIntelligenceEngine | None = None) -> None:
        self._engine = engine or DecisionIntelligenceEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a decision intelligence task.

        Expected task format::

            {
                "context": "...",
                "evidence_sources": [...],
                "constraints": [...],
                "objectives": [...],
                "risk_tolerance": "medium",
                "max_alternatives": 5,
                "include_explanation": true
            }

        Returns:
            DecisionResult as a JSON-serializable dict.
        """
        request = DecisionRequest(
            context=task.get("context", ""),
            evidence_sources=task.get("evidence_sources", []),
            constraints=task.get("constraints", []),
            objectives=task.get("objectives", []),
            risk_tolerance=task.get("risk_tolerance", "medium"),
            max_alternatives=task.get("max_alternatives", 5),
            include_explanation=task.get("include_explanation", True),
        )
        result = self._engine.evaluate(request)
        return result.to_dict()
