import logging
from dataclasses import dataclass, field
from typing import Any

from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


@dataclass
class DebateArgument:
    agent: str
    proposal: str
    reasoning: str
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class DebateResult:
    id: str
    topic: str
    arguments: list[DebateArgument] = field(default_factory=list)
    winner: str | None = None
    winning_proposal: str | None = None
    synthesis: str | None = None
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class DebateEngine:
    def __init__(self):
        self._debates: dict[str, DebateResult] = {}

    async def conduct_debate(self, topic: str, agents: list[str], rounds: int = 2) -> DebateResult:
        debate_id = f"debate-{len(self._debates)}"
        debate = DebateResult(id=debate_id, topic=topic)
        arguments: list[DebateArgument] = []
        for agent in agents:
            arg = await self._generate_argument(topic, agent, arguments)
            arguments.append(arg)
        debate.arguments = arguments
        winner, synthesis, confidence = await self._judge_debate(topic, arguments)
        debate.winner = winner
        debate.winning_proposal = next((a.proposal for a in arguments if a.agent == winner), None)
        debate.synthesis = synthesis
        debate.confidence = confidence
        self._debates[debate_id] = debate
        return debate

    async def _generate_argument(self, topic: str, agent: str, existing_args: list[DebateArgument]) -> DebateArgument:
        prompt = f"You are the {agent} agent. Provide your proposal for: {topic}\n"
        if existing_args:
            prompt += "\nOther proposals:\n"
            for arg in existing_args:
                prompt += f"- {arg.agent}: {arg.proposal}\n"
            prompt += "\nProvide a strong argument considering other proposals. Output JSON: {\"proposal\": str, \"reasoning\": str, \"strengths\": [str], \"weaknesses\": [str], \"confidence\": float}"
        response = model_router.complete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_MODEL,
            temperature=0.7,
            max_tokens=512,
        )
        import json
        try:
            data = json.loads(response.choices[0].message.content)
            return DebateArgument(
                agent=agent,
                proposal=data.get("proposal", ""),
                reasoning=data.get("reasoning", ""),
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                confidence=data.get("confidence", 0.5),
            )
        except (json.JSONDecodeError, AttributeError):
            return DebateArgument(agent=agent, proposal=topic, reasoning="", confidence=0.5)

    async def _judge_debate(self, topic: str, arguments: list[DebateArgument]) -> tuple[str | None, str, float]:
        prompt = (
            f"Judge the debate on: {topic}\n\n"
            "Proposals:\n"
        )
        for arg in arguments:
            prompt += f"- {arg.agent}: {arg.proposal} (confidence: {arg.confidence})\n"
        prompt += (
            "\nSelect the best proposal and provide a synthesis.\n"
            "Output JSON: {\"winner\": str, \"synthesis\": str, \"confidence\": float}"
        )
        response = model_router.complete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
            max_tokens=512,
        )
        import json
        try:
            data = json.loads(response.choices[0].message.content)
            return data.get("winner"), data.get("synthesis", ""), data.get("confidence", 0.0)
        except (json.JSONDecodeError, AttributeError):
            return None, "", 0.0


debate_engine = DebateEngine()
