"""
Monitoring Configurator
=======================

Configures monitoring, alerting, and observability stacks.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.schemas import ImprovementType, Problem, Solution

logger = logging.getLogger(__name__)

MONITORING_STACKS: dict[str, dict[str, Any]] = {
    "prometheus": {
        "metrics": ["cpu", "memory", "requests", "errors"],
        "scrape_interval": "15s",
        "retention": "15d",
        "alerting": True,
    },
    "grafana": {
        "dashboards": ["infrastructure", "application", "business"],
        "alerting": True,
        "sso": True,
    },
    "opentelemetry": {
        "traces": True,
        "metrics": True,
        "logs": True,
        "sampling": "1%",
    },
}


class MonitoringConfigurator:
    """Configures monitoring and observability."""

    def configure(self, service_name: str, stack: str = "prometheus") -> dict[str, Any]:
        config = MONITORING_STACKS.get(stack, MONITORING_STACKS["prometheus"])
        return {
            "service": service_name,
            "stack": stack,
            "config": config,
            "features": ["metrics_collection", "alerting", "dashboards", "log_aggregation"],
        }

    def suggest_improvements(self, current_config: dict[str, Any]) -> list[Solution]:
        solutions: list[Solution] = []
        features = current_config.get("features", [])

        if "alerting" not in features:
            solutions.append(Solution(
                problem_id=f"{current_config.get('service', 'unknown')}-missing-alerting",
                solution_type=ImprovementType.MONITORING.value,
                description="Tambahkan alerting ke monitoring stack.",
                estimated_effort="medium",
                risk="low",
                tests_required=True,
                confidence=0.9,
            ))

        if "log_aggregation" not in features:
            solutions.append(Solution(
                problem_id=f"{current_config.get('service', 'unknown')}-missing-logs",
                solution_type=ImprovementType.MONITORING.value,
                description="Tambahkan agregasi log untuk observabilitas.",
                estimated_effort="medium",
                risk="low",
                tests_required=True,
                confidence=0.85,
            ))

        return solutions
