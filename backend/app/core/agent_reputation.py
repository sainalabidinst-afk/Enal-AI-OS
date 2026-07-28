import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    QUALITY = "quality"
    SPEED = "speed"
    SUCCESS_RATE = "success_rate"
    COST = "cost"
    HALLUCINATION_RATE = "hallucination_rate"
    LATENCY = "latency"


@dataclass
class AgentReputation:
    agent_id: str
    metrics: dict[MetricType, float] = field(default_factory=dict)
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def record_task(self, success: bool, quality_score: float, latency_ms: float, cost: float):
        self.total_tasks += 1
        if success:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1
        self.metrics[MetricType.QUALITY] = (self.metrics.get(MetricType.QUALITY, 0.0) * (self.total_tasks - 1) + quality_score) / self.total_tasks
        self.metrics[MetricType.SUCCESS_RATE] = self.successful_tasks / self.total_tasks if self.total_tasks > 0 else 0.0
        self.metrics[MetricType.LATENCY] = (self.metrics.get(MetricType.LATENCY, 0.0) * (self.total_tasks - 1) + latency_ms) / self.total_tasks
        self.metrics[MetricType.COST] = (self.metrics.get(MetricType.COST, 0.0) * (self.total_tasks - 1) + cost) / self.total_tasks
        self.last_updated = datetime.utcnow()

    def get_score(self) -> float:
        if self.total_tasks == 0:
            return 5.0
        quality = self.metrics.get(MetricType.QUALITY, 5.0)
        success = self.metrics.get(MetricType.SUCCESS_RATE, 0.5)
        return (quality + success * 10) / 2


class AgentReputationManager:
    def __init__(self):
        self._reputations: dict[str, AgentReputation] = {}

    def get_or_create(self, agent_id: str) -> AgentReputation:
        if agent_id not in self._reputations:
            self._reputations[agent_id] = AgentReputation(agent_id=agent_id)
        return self._reputations[agent_id]

    def record(self, agent_id: str, success: bool, quality_score: float, latency_ms: float, cost: float):
        rep = self.get_or_create(agent_id)
        rep.record_task(success, quality_score, latency_ms, cost)

    def get_best_agent(self, capability: str, agents: list[str]) -> str | None:
        scored = []
        for agent_id in agents:
            rep = self.get_or_create(agent_id)
            scored.append((rep.get_score(), agent_id))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else None

    def get_leaderboard(self, limit: int = 10) -> list[dict[str, Any]]:
        ranked = sorted(self._reputations.values(), key=lambda r: r.get_score(), reverse=True)
        return [
            {
                "agent_id": r.agent_id,
                "score": r.get_score(),
                "total_tasks": r.total_tasks,
                "success_rate": r.metrics.get(MetricType.SUCCESS_RATE, 0.0),
                "quality": r.metrics.get(MetricType.QUALITY, 0.0),
                "cost_avg": r.metrics.get(MetricType.COST, 0.0),
            }
            for r in ranked[:limit]
        ]


agent_reputation = AgentReputationManager()
