"""
DevOps Engine
=============

Upgraded engine with typed contracts, pipeline generation, infrastructure design,
deployment planning, monitoring configuration, and project scanning.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.deployment_planner import DeploymentPlanner
from apps.devops_assistant.infrastructure_designer import InfrastructureDesigner
from apps.devops_assistant.monitoring_configurator import MonitoringConfigurator
from apps.devops_assistant.pipeline_generator import PipelineGenerator
from apps.devops_assistant.project_scanner import DevOpsProjectScanner
from apps.devops_assistant.schemas import ProjectAnalysis

logger = logging.getLogger(__name__)


class DevOpsEngine:
    """Upgraded DevOps engine with typed contracts."""

    def __init__(self) -> None:
        self.pipeline_generator = PipelineGenerator()
        self.infrastructure_designer = InfrastructureDesigner()
        self.deployment_planner = DeploymentPlanner()
        self.monitoring_configurator = MonitoringConfigurator()
        self.project_scanner = DevOpsProjectScanner()

    async def generate_pipeline(self, service_name: str, platform: str = "github_actions") -> dict[str, Any]:
        return self.pipeline_generator.generate(service_name, platform)

    async def design_infrastructure(self, service_name: str, platform: str = "kubernetes") -> dict[str, Any]:
        return self.infrastructure_designer.design(service_name, platform)

    async def plan_deployment(self, service_name: str, strategy: str = "rolling") -> dict[str, Any]:
        return self.deployment_planner.plan(service_name, strategy)

    async def configure_monitoring(self, service_name: str, stack: str = "prometheus") -> dict[str, Any]:
        return self.monitoring_configurator.configure(service_name, stack)

    def scan_project(self, project_path: str) -> ProjectAnalysis:
        return self.project_scanner.scan(project_path)

    def suggest_pipeline_improvements(self, pipeline: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "problem_id": s.problem_id,
                "solution_type": s.solution_type,
                "description": s.description,
                "estimated_effort": s.estimated_effort,
                "risk": s.risk,
                "confidence": s.confidence,
            }
            for s in self.pipeline_generator.suggest_improvements(pipeline)
        ]

    def suggest_infrastructure_improvements(self, infra: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "problem_id": s.problem_id,
                "solution_type": s.solution_type,
                "description": s.description,
                "estimated_effort": s.estimated_effort,
                "risk": s.risk,
                "confidence": s.confidence,
            }
            for s in self.infrastructure_designer.suggest_improvements(infra)
        ]

    def suggest_deployment_improvements(self, plan: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "problem_id": s.problem_id,
                "solution_type": s.solution_type,
                "description": s.description,
                "estimated_effort": s.estimated_effort,
                "risk": s.risk,
                "confidence": s.confidence,
            }
            for s in self.deployment_planner.suggest_improvements(plan)
        ]

    def suggest_monitoring_improvements(self, config: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "problem_id": s.problem_id,
                "solution_type": s.solution_type,
                "description": s.description,
                "estimated_effort": s.estimated_effort,
                "risk": s.risk,
                "confidence": s.confidence,
            }
            for s in self.monitoring_configurator.suggest_improvements(config)
        ]


devops_engine = DevOpsEngine()
