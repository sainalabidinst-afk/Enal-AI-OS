import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


class ReasoningStrategy(str, Enum):
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"


@dataclass
class Hypothesis:
    id: str
    description: str
    confidence: float = 0.0
    evidence: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningChain:
    id: str
    problem: str
    hypotheses: list[Hypothesis] = field(default_factory=list)
    selected_hypothesis_id: str | None = None
    reasoning_steps: list[str] = field(default_factory=list)
    conclusion: str | None = None
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class ReasoningEngine:
    def __init__(self):
        self._chains: dict[str, ReasoningChain] = {}

    async def generate_hypotheses(self, problem: str, num_hypotheses: int = 3) -> list[Hypothesis]:
        prompt = (
            f"Given the following problem, generate {num_hypotheses} distinct hypotheses or solution approaches.\n"
            f"Problem: {problem}\n\n"
            "For each hypothesis, provide:\n"
            "- A clear description\n"
            "- Key assumptions\n"
            "- Supporting evidence\n"
            "- Confidence level (0-1)\n\n"
            "Output as JSON array of objects."
        )
        response = await model_router.acomplete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.7,
            max_tokens=1024,
        )
        import json
        try:
            hypotheses_data = json.loads(response.choices[0].message.content)
            return [
                Hypothesis(
                    id=f"hyp-{i}",
                    description=h.get("description", ""),
                    confidence=h.get("confidence", 0.5),
                    evidence=h.get("evidence", []),
                    assumptions=h.get("assumptions", []),
                )
                for i, h in enumerate(hypotheses_data)
            ]
        except (json.JSONDecodeError, AttributeError):
            return [Hypothesis(id="hyp-0", description=problem, confidence=0.5)]

    async def reason(self, problem: str, hypotheses: list[Hypothesis]) -> ReasoningChain:
        chain = ReasoningChain(id=f"chain-{len(self._chains)}", problem=problem, hypotheses=hypotheses)
        prompt = (
            f"Analyze the following problem and hypotheses using structured reasoning.\n\n"
            f"Problem: {problem}\n\n"
            "Hypotheses:\n"
        )
        for i, h in enumerate(hypotheses):
            prompt += f"{i+1}. {h.description} (confidence: {h.confidence})\n"
        prompt += (
            "\nProvide a step-by-step reasoning chain, evaluate each hypothesis, "
            "select the best one, and state a conclusion.\n"
            "Output JSON: {\"reasoning_steps\": [str], \"selected_id\": str, \"conclusion\": str, \"confidence\": float}"
        )
        response = await model_router.acomplete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )
        import json
        try:
            result = json.loads(response.choices[0].message.content)
            chain.reasoning_steps = result.get("reasoning_steps", [])
            chain.selected_hypothesis_id = result.get("selected_id")
            chain.conclusion = result.get("conclusion")
            chain.confidence = result.get("confidence", 0.0)
        except (json.JSONDecodeError, AttributeError):
            chain.conclusion = problem
            chain.confidence = 0.5
        self._chains[chain.id] = chain
        return chain

    async def decide(self, chain: ReasoningChain) -> dict[str, Any]:
        if not chain.conclusion:
            return {"decision": chain.problem, "confidence": 0.0}
        return {
            "decision": chain.conclusion,
            "hypothesis": chain.selected_hypothesis_id,
            "confidence": chain.confidence,
            "reasoning": chain.reasoning_steps,
        }


reasoning_engine = ReasoningEngine()
