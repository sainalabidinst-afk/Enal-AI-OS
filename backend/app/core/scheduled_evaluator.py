"""
Scheduled evaluator for periodic quality checks.

Runs evaluations on a schedule and stores results.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from backend.app.core.evaluator_engine import evaluator_engine

logger = logging.getLogger(__name__)


class ScheduledEvaluator:
    """Run evaluations on a schedule."""

    def __init__(self) -> None:
        self._results: list[dict[str, Any]] = []

    async def run_evaluation(
        self,
        output: str,
        criteria: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = await evaluator_engine.evaluate(output, criteria)
        result["timestamp"] = datetime.now(UTC).isoformat()
        self._results.append(result)
        return result

    def get_results(self) -> list[dict[str, Any]]:
        return list(self._results)


scheduled_evaluator = ScheduledEvaluator()
