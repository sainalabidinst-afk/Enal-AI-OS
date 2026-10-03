"""
Evaluator engine for running evaluations.

Runs scheduled evaluations and aggregates metrics.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.core.quality_scorer import quality_scorer

logger = logging.getLogger(__name__)


class EvaluatorEngine:
    """Run evaluations against agent/tool outputs."""

    async def evaluate(self, output: str, criteria: dict[str, Any] | None = None) -> dict[str, Any]:
        result = quality_scorer.score(output, criteria)
        return {
            "score": result.score,
            "criteria": result.criteria,
            "feedback": result.feedback,
        }


evaluator_engine = EvaluatorEngine()
