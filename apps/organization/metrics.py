"""
Organizational Metrics
=======================

Measures organizational performance, not just individual agents.
Tracks project completion time, quality, token cost, collaboration rate, and team success rate.
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ProjectMetrics:
    project_id: str
    team_id: str
    start_time: datetime
    end_time: datetime | None = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    quality_score: float = 0.0
    collaboration_score: float = 0.0
    agents_involved: list[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.utcnow() - self.start_time).total_seconds()

    @property
    def success_rate(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return self.tasks_completed / total if total > 0 else 0.0


@dataclass
class TeamMetrics:
    team_id: str
    projects_completed: int = 0
    projects_failed: int = 0
    average_duration_seconds: float = 0.0
    average_quality: float = 0.0
    average_cost: float = 0.0
    collaboration_score: float = 0.0


class OrganizationalMetrics:
    """Tracks organizational-level metrics."""

    def __init__(self):
        self._project_metrics: dict[str, ProjectMetrics] = {}
        self._team_metrics: dict[str, TeamMetrics] = {}

    def start_project(self, project_id: str, team_id: str) -> ProjectMetrics:
        metrics = ProjectMetrics(
            project_id=project_id,
            team_id=team_id,
            start_time=datetime.utcnow(),
        )
        self._project_metrics[project_id] = metrics
        return metrics

    def end_project(self, project_id: str) -> ProjectMetrics | None:
        metrics = self._project_metrics.get(project_id)
        if metrics:
            metrics.end_time = datetime.utcnow()
            self._update_team_metrics(metrics)
        return metrics

    def record_task(self, project_id: str, success: bool, tokens: int = 0, cost: float = 0.0) -> None:
        metrics = self._project_metrics.get(project_id)
        if metrics:
            if success:
                metrics.tasks_completed += 1
            else:
                metrics.tasks_failed += 1
            metrics.total_tokens += tokens
            metrics.total_cost += cost

    def get_project_metrics(self, project_id: str) -> ProjectMetrics | None:
        return self._project_metrics.get(project_id)

    def get_team_metrics(self, team_id: str) -> TeamMetrics | None:
        return self._team_metrics.get(team_id)

    def _update_team_metrics(self, project_metrics: ProjectMetrics) -> None:
        team_id = project_metrics.team_id
        team = self._team_metrics.get(team_id)
        if not team:
            team = TeamMetrics(team_id=team_id)
            self._team_metrics[team_id] = team

        if project_metrics.success_rate >= 0.8:
            team.projects_completed += 1
        else:
            team.projects_failed += 1

        n = team.projects_completed + team.projects_failed
        team.average_duration_seconds = (
            (team.average_duration_seconds * (n - 1) + project_metrics.duration_seconds) / n
        )
        team.average_quality = (
            (team.average_quality * (n - 1) + project_metrics.quality_score) / n
        )
        team.average_cost = (
            (team.average_cost * (n - 1) + project_metrics.total_cost) / n
        )


organizational_metrics = OrganizationalMetrics()
