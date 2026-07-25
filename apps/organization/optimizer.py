"""
Workforce Optimizer
====================

Optimizes organization structure, team composition, model allocation, and budget.
Continuously improves the workforce based on metrics and learning.
"""

import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class OptimizationSuggestion:
    id: str
    category: str
    description: str
    expected_impact: str
    estimated_savings: float = 0.0
    priority: str = "medium"
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkforceOptimizer:
    """Optimizes workforce structure and resource allocation."""

    def __init__(self):
        self._suggestions: list[OptimizationSuggestion] = []
        self._optimization_history: list[dict[str, Any]] = []

    def optimize_team_composition(self, team_members: list[Any], task_requirements: dict[str, Any]) -> list[OptimizationSuggestion]:
        suggestions = []
        team_size = len(team_members)
        if team_size > 7:
            suggestions.append(OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="team_composition",
                description=f"Team size ({team_size}) exceeds optimal size (5-7). Consider splitting.",
                expected_impact="Improved coordination and reduced communication overhead",
                estimated_savings=team_size * 0.1,
                priority="high",
            ))
        if team_size < 2 and task_requirements.get("complexity", "medium") == "high":
            suggestions.append(OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="team_composition",
                description="Team size is too small for high-complexity task. Consider adding members.",
                expected_impact="Improved quality and reduced completion time",
                priority="high",
            ))
        return suggestions

    def optimize_model_allocation(self, worker_id: str, capability: str, current_model: str, cost_per_1k: float, quality_score: float) -> OptimizationSuggestion | None:
        if cost_per_1k > 0.001 and quality_score < 0.85:
            return OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="model_allocation",
                description=f"Worker {worker_id} using expensive model ({current_model}) for low-quality output. Consider cheaper alternative.",
                expected_impact="Reduced cost with minimal quality loss",
                estimated_savings=cost_per_1k * 100,
                priority="medium",
            )
        return None

    def optimize_budget(self, budget_status: dict[str, Any]) -> list[OptimizationSuggestion]:
        suggestions = []
        utilization = budget_status.get("utilization", 0)
        if utilization > 90:
            suggestions.append(OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="budget",
                description="Budget utilization is very high (>90%). Consider reducing team size or using cheaper models.",
                expected_impact="Prevent budget overrun",
                priority="critical",
            ))
        elif utilization < 30:
            suggestions.append(OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="budget",
                description="Budget utilization is low (<30%). Consider allocating more resources or reducing budget.",
                expected_impact="Better resource utilization",
                priority="low",
            ))
        return suggestions

    def should_retire_worker(self, worker_id: str, quality_score: float, reuse_rate: float, days_since_last_use: int) -> OptimizationSuggestion | None:
        if quality_score < 0.5 and days_since_last_use > 30:
            return OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="worker_retirement",
                description=f"Worker {worker_id} has low quality ({quality_score:.2f}) and hasn't been used in {days_since_last_use} days. Consider retiring.",
                expected_impact="Reduced maintenance cost and improved organization efficiency",
                estimated_savings=10.0,
                priority="medium",
            )
        if reuse_rate < 0.1 and days_since_last_use > 90:
            return OptimizationSuggestion(
                id=f"opt-{uuid.uuid4().hex[:8]}",
                category="worker_retirement",
                description=f"Worker {worker_id} has very low reuse rate ({reuse_rate:.2f}) and hasn't been used in {days_since_last_use} days. Consider retiring.",
                expected_impact="Reduced maintenance cost",
                estimated_savings=5.0,
                priority="low",
            )
        return None

    def get_suggestions(self, category: str | None = None) -> list[OptimizationSuggestion]:
        suggestions = list(self._suggestions)
        if category:
            suggestions = [s for s in suggestions if s.category == category]
        return suggestions

    def clear_suggestions(self) -> None:
        self._suggestions.clear()


workforce_optimizer = WorkforceOptimizer()
