"""
Infrastructure Engineer — Domain Engine orchestrator.

Orchestrates the full infrastructure engineering pipeline:
    1. Kubernetes Design — K8s cluster and workload design
    2. HA Cluster Design — High-availability cluster topology
    3. Storage Design — Block, file, object, distributed storage
    4. Disaster Recovery Planning — RPO/RTO, multi-site strategy
    5. Infrastructure Assessment — Gap analysis and recommendations

All infrastructure logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
from typing import Any

from apps.infrastructure_engineer.kubernetes_designer import KubernetesDesigner
from apps.infrastructure_engineer.ha_cluster_designer import HAClusterDesigner
from apps.infrastructure_engineer.storage_designer import StorageDesigner
from apps.infrastructure_engineer.disaster_recovery import DisasterRecoveryPlanner
from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    InfrastructureEngineerReport,
)

logger = logging.getLogger(__name__)


class InfrastructureEngineerEngine:
    """
    Orchestrates the full infrastructure engineering pipeline.

    Public API::

        engine = InfrastructureEngineerEngine()
        report = engine.design(request)
    """

    def __init__(self) -> None:
        self.k8s_designer = KubernetesDesigner()
        self.ha_cluster_designer = HAClusterDesigner()
        self.storage_designer = StorageDesigner()
        self.dr_planner = DisasterRecoveryPlanner()

    def design(self, request: InfrastructureEngineerRequest) -> InfrastructureEngineerReport:
        """
        Run the infrastructure engineering pipeline based on operation.

        Args:
            request: InfrastructureEngineerRequest with context, inputs, options.

        Returns:
            InfrastructureEngineerReport with all generated artifacts.
        """
        op = request.operation
        logger.info("Running infrastructure operation: %s", op.value)

        kubernetes_spec = None
        cluster_spec = None
        storage_specs: list[Any] = []
        dr_plan = None
        recommendations: list[str] = []
        cost_estimate: dict[str, float] = {}
        security_hardening: list[str] = []
        compliance_status: dict[str, bool] = {}
        quality_score = 0.85

        if op == InfrastructureEngineerRequest.operation.kubernetes_design:
            kubernetes_spec = self.k8s_designer.design_cluster(request)
            recommendations = self.k8s_designer.get_recommendations(kubernetes_spec)
            cost_estimate = self.k8s_designer.estimate_cost(kubernetes_spec)
            security_hardening = self.k8s_designer.get_security_hardening(kubernetes_spec)
            quality_score = self.k8s_designer.score_quality(kubernetes_spec)

        elif op == InfrastructureEngineerRequest.operation.ha_cluster_design:
            cluster_spec = self.ha_cluster_designer.design_cluster(request)
            recommendations = self.ha_cluster_designer.get_recommendations(cluster_spec)
            cost_estimate = self.ha_cluster_designer.estimate_cost(cluster_spec)
            security_hardening = self.ha_cluster_designer.get_security_hardening(cluster_spec)
            quality_score = self.ha_cluster_designer.score_quality(cluster_spec)

        elif op == InfrastructureEngineerRequest.operation.storage_design:
            storage_specs = self.storage_designer.design_storage(request)
            recommendations = self.storage_designer.get_recommendations(storage_specs)
            cost_estimate = self.storage_designer.estimate_cost(storage_specs)
            security_hardening = self.storage_designer.get_security_hardening(storage_specs)
            quality_score = self.storage_designer.score_quality(storage_specs)

        elif op == InfrastructureEngineerRequest.operation.disaster_recovery_plan:
            dr_plan = self.dr_planner.plan(request)
            recommendations = self.dr_planner.get_recommendations(dr_plan)
            cost_estimate = self.dr_planner.estimate_cost(dr_plan)
            security_hardening = self.dr_planner.get_security_hardening(dr_plan)
            compliance_status = self.dr_planner.check_compliance(dr_plan)
            quality_score = self.dr_planner.score_quality(dr_plan)

        elif op == InfrastructureEngineerRequest.operation.infrastructure_assessment:
            kubernetes_spec = self.k8s_designer.design_cluster(request)
            cluster_spec = self.ha_cluster_designer.design_cluster(request)
            storage_specs = self.storage_designer.design_storage(request)
            dr_plan = self.dr_planner.plan(request)
            recommendations = (
                self.k8s_designer.get_recommendations(kubernetes_spec)
                + self.ha_cluster_designer.get_recommendations(cluster_spec)
                + self.storage_designer.get_recommendations(storage_specs)
                + self.dr_planner.get_recommendations(dr_plan)
            )
            cost_estimate = self._aggregate_costs(
                self.k8s_designer.estimate_cost(kubernetes_spec),
                self.ha_cluster_designer.estimate_cost(cluster_spec),
                self.storage_designer.estimate_cost(storage_specs),
                self.dr_planner.estimate_cost(dr_plan),
            )
            security_hardening = (
                self.k8s_designer.get_security_hardening(kubernetes_spec)
                + self.ha_cluster_designer.get_security_hardening(cluster_spec)
                + self.storage_designer.get_security_hardening(storage_specs)
                + self.dr_planner.get_security_hardening(dr_plan)
            )
            compliance_status = self.dr_planner.check_compliance(dr_plan) if dr_plan else {}
            quality_score = (
                self.k8s_designer.score_quality(kubernetes_spec)
                + self.ha_cluster_designer.score_quality(cluster_spec)
                + self.storage_designer.score_quality(storage_specs)
                + self.dr_planner.score_quality(dr_plan)
            ) / 4.0

        explanation = self._generate_explanation(op, quality_score, recommendations)
        return InfrastructureEngineerReport(
            request_id=request.request_id,
            operation=op.value,
            kubernetes_spec=kubernetes_spec,
            cluster_spec=cluster_spec,
            storage_specs=storage_specs,
            dr_plan=dr_plan,
            cost_estimate=cost_estimate,
            security_hardening=security_hardening,
            compliance_status=compliance_status,
            recommendations=recommendations,
            quality_score=quality_score,
            explanation=explanation,
        )

    def _aggregate_costs(self, *cost_dicts: dict[str, float]) -> dict[str, float]:
        aggregated: dict[str, float] = {}
        for d in cost_dicts:
            for key, value in d.items():
                aggregated[key] = aggregated.get(key, 0.0) + value
        return aggregated

    def _generate_explanation(self, operation: Any, quality_score: float, recommendations: list[str]) -> str:
        op_name = operation.value if hasattr(operation, "value") else str(operation)
        recs_summary = f"{len(recommendations)} rekomendasi" if recommendations else "tidak ada rekomendasi"
        return (
            f"Desain infrastruktur untuk operasi '{op_name}' telah dihasilkan dengan skor kualitas "
            f"{quality_score:.0%}. {recs_summary} disertakan untuk peningkatan."
        )


infrastructure_engineer_engine = InfrastructureEngineerEngine()
