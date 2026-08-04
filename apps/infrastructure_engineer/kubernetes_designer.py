"""
Kubernetes Designer
====================

Designs Kubernetes cluster specifications, workload configurations,
network policies, and security settings.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    KubernetesSpec,
    NodeConfig,
    NetworkConfig,
    HighAvailabilityMode,
)

logger = logging.getLogger(__name__)

DEFAULT_NODE_CONFIGS: list[NodeConfig] = [
    NodeConfig(count=3, instance_type="t3.large", os_image="ubuntu-22.04"),
    NodeConfig(count=2, instance_type="t3.xlarge", os_image="ubuntu-22.04"),
]

DEFAULT_NETWORK_CONFIG = NetworkConfig(
    cidr="10.0.0.0/16",
    subnet_count=3,
    load_balancer_type="layer4",
    ingress_controller="nginx",
    dns_policy="cluster_first",
)


class KubernetesDesigner:
    """Designs Kubernetes cluster and workload specifications."""

    def design_cluster(self, request: InfrastructureEngineerRequest) -> KubernetesSpec:
        inputs = request.inputs
        cluster_name = inputs.get("cluster_name", request.business_context.project_name or "default-cluster")
        k8s_version = inputs.get("kubernetes_version", "1.28")
        node_count = inputs.get("node_count", 3)
        instance_type = inputs.get("instance_type", "t3.medium")
        availability = request.quality_attributes.availability_target

        if "99.99" in availability or "99.999" in availability:
            ha_mode = HighAvailabilityMode.active_active
            node_count = max(node_count, 5)
        elif "99.9" in availability:
            ha_mode = HighAvailabilityMode.active_standby
            node_count = max(node_count, 3)
        else:
            ha_mode = HighAvailabilityMode.n_plus_1
            node_count = max(node_count, 2)

        nodes = [
            NodeConfig(
                count=max(node_count // 2, 2),
                instance_type=instance_type,
                os_image="ubuntu-22.04",
                labels={"role": "worker"},
            ),
            NodeConfig(
                count=max(node_count // 3, 1),
                instance_type=instance_type,
                os_image="ubuntu-22.04",
                labels={"role": "control-plane"},
                taints=["node-role.kubernetes.io/control-plane:NoSchedule"],
            ),
        ]

        network = NetworkConfig(
            cidr=inputs.get("network_cidr", "10.0.0.0/16"),
            subnet_count=inputs.get("subnet_count", 3),
            load_balancer_type=inputs.get("load_balancer_type", "layer4"),
            ingress_controller=inputs.get("ingress_controller", "nginx"),
            dns_policy=inputs.get("dns_policy", "cluster_first"),
        )

        return KubernetesSpec(
            cluster_name=cluster_name,
            kubernetes_version=k8s_version,
            network_policy=True,
            rbac_enabled=True,
            pod_security_standard="restricted",
            resource_quotas=True,
            limit_ranges=True,
            nodes=nodes,
            network=network,
        )

    def get_recommendations(self, spec: KubernetesSpec) -> list[str]:
        recs: list[str] = []
        if spec.kubernetes_version < "1.26":
            recs.append("Tingkatkan Kubernetes ke versi stabil terbaru untuk patch keamanan")
        if not spec.network_policy:
            recs.append("Aktifkan NetworkPolicy untuk isolasi namespace")
        if not spec.resource_quotas:
            recs.append("Aktifkan ResourceQuota untuk mencegah exhaust namespace")
        if not spec.limit_ranges:
            recs.append("Aktifkan LimitRange untuk default resource limits per container")
        for node in spec.nodes:
            for taint in node.taints:
                if "control-plane" not in taint:
                    recs.append(f"Evaluasi taint '{taint}' pada node — pertimbangkan tolerasi")
        if not any("monitoring" in n.labels.get("role", "") for n in spec.nodes):
            recs.append("Tambahkan node khusus monitoring dengan label role=monitoring")
        return recs

    def estimate_cost(self, spec: KubernetesSpec) -> dict[str, float]:
        monthly = 0.0
        node_costs: dict[str, float] = {}
        for node in spec.nodes:
            if "xlarge" in node.instance_type:
                cost_per_node = 150.0
            elif "large" in node.instance_type:
                cost_per_node = 80.0
            else:
                cost_per_node = 40.0
            node_costs[node.instance_type] = node_costs.get(node.instance_type, 0.0) + cost_per_node * node.count
            monthly += cost_per_node * node.count
        node_costs["total_monthly"] = monthly
        return node_costs

    def get_security_hardening(self, spec: KubernetesSpec) -> list[str]:
        return [
            f"PodSecurityStandard '{spec.pod_security_standard}' diaktifkan",
            "RBAC diaktifkan — review ServiceAccount dan RoleBinding",
            "NetworkPolicy diaktifkan — default deny all traffic antar namespace",
            "SeccompProfile RuntimeDefault diterapkan ke PodSecurity Admission",
            "Etcd dienkripsi di rest (encryption-at-rest)",
            "Audit logging diaktifkan untuk API server",
            "Image scanning (Trivy/Grype) diaktifkan di admission webhook",
        ]

    def score_quality(self, spec: KubernetesSpec) -> float:
        score = 0.7
        if spec.network_policy:
            score += 0.05
        if spec.rbac_enabled:
            score += 0.05
        if spec.resource_quotas:
            score += 0.05
        if spec.limit_ranges:
            score += 0.05
        if spec.nodes:
            score += 0.05
        return min(score, 1.0)
