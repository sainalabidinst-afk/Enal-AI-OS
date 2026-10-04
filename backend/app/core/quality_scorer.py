"""
Evaluation engine for scoring agent/tool outputs.

Provides quality scoring and evaluation metrics for AI outputs.
Uses LLM-based evaluation when available, falls back to heuristic scoring.
Multi-dimensional scoring with vendor-specific rule validation.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from backend.app.core.evaluation_schema import (
    DIMENSION_RUBRICS,
    EVALUATION_DIMENSIONS,
    DimensionScore,
    EvaluationCase,
    EvaluationDimension,
    EvaluationResult,
)
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


class QualityScorer:
    """Score quality of agent/tool outputs using LLM-based multi-dimensional evaluation."""

    async def score(
        self,
        output: str,
        criteria: dict[str, Any] | None = None,
        vendor: str | None = None,
        scenario: str | None = None,
    ) -> EvaluationResult:
        criteria = criteria or {}
        result = await self._llm_evaluate(output, criteria, vendor, scenario)
        if result is None:
            result = self._heuristic_evaluate(output, criteria)
        return result

    async def score_case(self, case: EvaluationCase, output: str) -> EvaluationResult:
        result = await self.score(
            output,
            criteria=case.rubric,
            vendor=case.vendor,
            scenario=case.scenario,
        )
        result.metadata["case_id"] = case.case_id
        result.metadata["scenario"] = case.scenario
        result.metadata["vendor"] = case.vendor
        result.metadata["domain"] = case.domain
        return result

    async def _llm_evaluate(
        self,
        output: str,
        criteria: dict[str, Any],
        vendor: str | None,
        scenario: str | None,
    ) -> EvaluationResult | None:
        try:
            dimensions_str = ", ".join(d.value for d in EVALUATION_DIMENSIONS)
            prompt = (
                "Evaluate the following AI output across multiple dimensions.\n"
                "Return JSON with this exact schema:\n"
                '{"overall_score": float (0-1), '
                '"dimensions": {"dimension_name": {"score": float, "feedback": str}}, '
                '"insights": [str]}\n\n'
                f"Dimensions to evaluate: {dimensions_str}\n"
                f"Criteria: {json.dumps(criteria)}\n"
                f"Vendor: {vendor or 'generic'}\n"
                f"Scenario: {scenario or 'generic'}\n\n"
                f"Output to evaluate:\n{output}\n"
            )
            response = await model_router.acomplete(
                [{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=512,
            )
            content = response.choices[0].message.content if response else ""
            try:
                data = json.loads(content)
                overall_score = min(max(float(data.get("overall_score", 0.0)), 0.0), 1.0)
                dimension_scores = []
                for dim_name, dim_data in data.get("dimensions", {}).items():
                    try:
                        dim_enum = EvaluationDimension(dim_name)
                        score = min(max(float(dim_data.get("score", 0.0)), 0.0), 1.0)
                        dimension_scores.append(
                            DimensionScore(
                                dimension=dim_enum,
                                score=score,
                                weight=DIMENSION_RUBRICS[dim_enum]["weight"],
                                feedback=dim_data.get("feedback", ""),
                            )
                        )
                    except ValueError:
                        continue
                insights = data.get("insights", [])
                result = EvaluationResult(
                    overall_score=overall_score,
                    dimension_scores=dimension_scores,
                    feedback="; ".join(insights) if insights else "LLM evaluation completed",
                )
                result.calculate_overall()
                return result
            except (json.JSONDecodeError, ValueError, KeyError):
                pass
        except Exception as exc:
            logger.warning("LLM evaluation failed, falling back to heuristic: %s", exc)
        return None

    def _heuristic_evaluate(self, output: str, criteria: dict[str, Any]) -> EvaluationResult:
        dimension_scores = []
        for dim in EVALUATION_DIMENSIONS:
            score = 0.0
            if dim.value in criteria:
                score = min(float(criteria[dim.value]) * 0.7 + 0.3, 1.0)
            dimension_scores.append(
                DimensionScore(
                    dimension=dim,
                    score=score,
                    weight=DIMENSION_RUBRICS[dim]["weight"],
                    feedback=f"Heuristic score for {dim.value}",
                )
            )
        result = EvaluationResult(dimension_scores=dimension_scores, feedback="Heuristic fallback")
        result.calculate_overall()
        return result


quality_scorer = QualityScorer()
