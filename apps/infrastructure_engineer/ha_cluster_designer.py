"""
HA Cluster Designer
====================

Designs high-availability cluster topologies with failover configurations,
load balancers, and quorum management.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    ClusterSpec,
    NodeConfig,
    FailoverConfig,
    HighAvailabilityMode,
)

logger = logging.getLogger(__name__)

DEFAULT_FAILOVER_CONFIG = FailoverConfig(
    mode=HighAvailabilityMode.active_passive,
    heartbeat_interval_seconds=5,
    failover_timeout_seconds=30,
    quorum_required=True,
    fencing_mechanism="stonith",
)


class HAClusterDesigner:
    """Designs high-availability cluster specifications."""

    def design_cluster(self, request: InfrastructureEngineerRequest) -> ClusterSpec:
        inputs = request.inputs
        cluster_name = inputs.get("cluster_name", request.business_context.project_name or "ha-cluster")
        availability = request.quality_attributes.availability_target
        node_count = inputs.get("node_count", 3)
        node_type = inputs.get("instance_type", "t3.large")

        if "99.99" in availability or "99.999" in availability:
            ha_mode = HighAvailabilityMode.active_active
            node_count = max(node_count, 5)
            failover = FailoverConfig(
                mode=HighAvailabilityMode.active_active,
                heartbeat_interval_seconds=2,
                failover_timeout_seconds=10,
                quorum_required=True,
                fencing_mechanism="stonith",
            )
        elif "99.9" in availability:
            ha_mode = HighAvailabilityMode.active_standby
            node_count = max(node_count, 3)
            failover = FailoverConfig(
                mode=HighAvailabilityMode.active_standby,
                heartbeat_interval_seconds=5,
                failover_timeout_seconds=30,
                quorum_required=True,
                fencing_mechanism="stonith",
            )
        else:
            ha_mode = HighAvailabilityMode.n_plus_1
            failover = FailoverConfig(
                mode=HighAvailabilityMode.n_plus_1,
                heartbeat_interval_seconds=10,
                failover_timeout_seconds=60,
                quorum_required=False,
                fencing_mechanism="software_fence",
            )

        nodes = [
            NodeConfig(
                count=node_count,
                instance_type=node_type,
                os_image="ubuntu-22.04",
                labels={"role": "cluster-node"},
            )
        ]

        shared_storage = inputs.get("shared_storage", "ceph")

        return ClusterSpec(
            cluster_name=cluster_name,
            nodes=nodes,
            ha_mode=ha_mode,
            shared_storage=shared_storage,
            failover=failover,
            load_balancer=inputs.get("load_balancer", "haproxy"),
        )

    def get_recommendations(self, spec: ClusterSpec) -> list[str]:
        recs: list[str] = []
        if spec.ha_mode == HighAvailabilityMode.active_active:
            recs.append("Verifikasi aplikasi mendukung konkurensi stateful untuk active-active")
        if spec.failover.failover_timeout_seconds > 60:
            recs.append("Failover timeout terlalu tinggi — pertimbangkan heartbeat interval lebih pendek")
        if not spec.failover.quorum_required and spec.nodes[0].count > 2:
            recs.append("Aktifkan quorum untuk mencegah split-brain pada cluster dengan >2 node")
        if "ceph" not in spec.shared_storage and spec.ha_mode != HighAvailabilityMode.n_plus_1:
            recs.append("Pertimbangkan Ceph untuk shared storage di mode HA yang ketat")
        return recs

    def estimate_cost(self, spec: ClusterSpec) -> dict[str, float]:
        node_cost = 0.0
        instance = spec.nodes[0].instance_type if spec.nodes else "t3.large"
        if "xlarge" in instance:
            node_cost = 150.0
        elif "large" in instance:
            node_cost = 80.0
        else:
            node_cost = 40.0
        total = node_cost * sum(n.count for n in spec.nodes)
        lb_cost = 30.0 if "haproxy" in spec.load_balancer else 50.0
        return {
            f"node_{instance}": total,
            "load_balancer": lb_cost,
            "total_monthly": total + lb_cost,
        }

    def get_security_hardening(self, spec: ClusterSpec) -> list[str]:
        return [
            f"Fencing mechanism: {spec.failover.fencing_mechanism} diaktifkan",
            f"Heartbeat interval: {spec.failover.heartbeat_interval_seconds}s — monitoring active",
            f"Quorum: {'wajib' if spec.failover.quorum_required else 'opsional'} — split-brain prevention",
            "Corosync/Pacemaker dienkripsi — mencegah sniffing heartbeat",
            "Shared storage dienkripsi (LUKS atau storage-level encryption)",
            "Cluster communication melalui jaringan pribadi/VPC",
        ]

    def score_quality(self, spec: ClusterSpec) -> float:
        score = 0.7
        if spec.failover.quorum_required:
            score += 0.05
        if spec.failover.failover_timeout_seconds <= 30:
            score += 0.05
        if spec.failover.fencing_mechanism == "stonith":
            score += 0.1
        if spec.nodes:
            score += 0.05
        return min(score, 1.0)
