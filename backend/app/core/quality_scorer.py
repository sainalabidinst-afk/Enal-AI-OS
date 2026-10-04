"""
Evaluation engine for scoring agent/tool outputs.

Provides quality scoring and evaluation metrics for AI outputs.
Uses LLM-based evaluation when available, falls back to heuristic scoring.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


class EvaluationResult:
    def __init__(
        self,
        score: float,
        criteria: dict[str, Any],
        feedback: str = "",
    ) -> None:
        self.score = score
        self.criteria = criteria
        self.feedback = feedback


class QualityScorer:
    """Score quality of agent/tool outputs using LLM-based evaluation."""

    async def score(self, output: str, criteria: dict[str, Any] | None = None) -> EvaluationResult:
        criteria = criteria or {}
        try:
            prompt = (
                "Evaluate the following AI output against the provided criteria.\n"
                "Return JSON: {\"score\": float (0-1), \"feedback\": str}\n\n"
                f"Criteria: {criteria}\n"
                f"Output to evaluate:\n{output}\n"
            )
            response = await model_router.acomplete(
                [{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=256,
            )
            import json

            content = response.choices[0].message.content if response else ""
            try:
                result = json.loads(content)
                score = float(result.get("score", 0.0))
                feedback = result.get("feedback", "LLM evaluation completed")
                return EvaluationResult(
                    score=min(max(score, 0.0), 1.0),
                    criteria=criteria,
                    feedback=feedback,
                )
            except (json.JSONDecodeError, ValueError):
                pass
        except Exception as exc:
            logger.warning("LLM evaluation failed, falling back to heuristic: %s", exc)

        score = 0.0
        if "relevance" in criteria:
            score += 0.25
        if "accuracy" in criteria:
            score += 0.25
        if "coherence" in criteria:
            score += 0.25
        if "completeness" in criteria:
            score += 0.25
        return EvaluationResult(
            score=min(score, 1.0),
            criteria=criteria,
            feedback="Heuristic fallback score (LLM evaluation unavailable)",
        )


quality_scorer = QualityScorer()
