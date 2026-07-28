import logging
from dataclasses import dataclass, field
from typing import Any

from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


@dataclass
class DecisionOption:
    id: str
    description: str
    utility: float = 0.0
    risk: float = 0.0
    cost: float = 0.0
    confidence: float = 0.0
    expected_value: float = 0.0
    reward: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionResult:
    selected_option_id: str | None
    selected_description: str | None
    confidence: float = 0.0
    expected_value: float = 0.0
    reasoning: str = ""
    all_options: list[dict[str, Any]] = field(default_factory=list)


class DecisionEngine:
    async def decide(self, options: list[DecisionOption], context: dict[str, Any] | None = None) -> DecisionResult:
        if not options:
            return DecisionResult(selected_option_id=None, selected_description=None)
        if len(options) == 1:
            opt = options[0]
            return DecisionResult(selected_option_id=opt.id, selected_description=opt.description, confidence=opt.confidence, expected_value=opt.expected_value)

        scored = []
        for opt in options:
            opt.expected_value = self._calculate_expected_value(opt)
            scored.append((opt.expected_value, opt))
        scored.sort(key=lambda x: x[0], reverse=True)
        best = scored[0][1]
        return DecisionResult(
            selected_option_id=best.id,
            selected_description=best.description,
            confidence=best.confidence,
            expected_value=best.expected_value,
            reasoning=f"Selected based on expected value: {best.expected_value:.2f}",
            all_options=[{"id": o.id, "description": o.description, "expected_value": o.expected_value, "confidence": o.confidence} for _, o in scored],
        )

    def _calculate_expected_value(self, option: DecisionOption) -> float:
        return (option.utility * option.confidence) - (option.risk + option.cost)

    async def evaluate_options(self, task_description: str, alternatives: list[str]) -> list[DecisionOption]:
        options = []
        for i, alt in enumerate(alternatives):
            scores = await self._score_alternative(task_description, alt)
            option = DecisionOption(
                id=f"opt-{i}",
                description=alt,
                utility=scores.get("utility", 0.5),
                risk=scores.get("risk", 0.5),
                cost=scores.get("cost", 0.5),
                confidence=scores.get("confidence", 0.5),
            )
            option.expected_value = self._calculate_expected_value(option)
            options.append(option)
        return options

    async def _score_alternative(self, task_description: str, alternative: str) -> dict[str, float]:
        prompt = (
            f"Score the following alternative solution for the task.\n"
            f"Task: {task_description}\n"
            f"Alternative: {alternative}\n\n"
            "Output JSON with scores 0-1: {\"utility\": float, \"risk\": float, \"cost\": float, \"confidence\": float}"
        )
        response = model_router.complete([{"role": "user", "content": prompt}], temperature=0.3, max_tokens=256)
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except (json.JSONDecodeError, AttributeError):
            return {"utility": 0.5, "risk": 0.5, "cost": 0.5, "confidence": 0.5}


decision_engine = DecisionEngine()
