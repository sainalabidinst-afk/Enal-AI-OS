"""
Database Engineer — Replication Planner.

Designs replication strategies for high availability and
performance: primary-replica, multi-primary, and leaderless topologies.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.database_engineer.schemas import (
    WorkloadProfile,
    DatabaseType,
    ReplicationDesign,
)

logger = logging.getLogger(__name__)


class ReplicationPlanner:
    """
    Designs database replication strategies.

    Usage::

        planner = ReplicationPlanner()
        design = planner.design(workload, database_type)
    """

    def design(
        self,
        workload: WorkloadProfile | None,
        database_type: DatabaseType = DatabaseType.postgresql,
    ) -> ReplicationDesign:
        """
        Design a replication topology.

        Args:
            workload: Workload profile with read/write ratio, QPS.
            database_type: Target database type.

        Returns:
            ReplicationDesign with topology and setup steps.
        """
        if not workload:
            return self._default_design(database_type)

        read_ratio = workload.read_write_ratio
        qps = workload.peak_qps
        data_gb = workload.data_volume_gb

        # Choose strategy based on workload.
        if read_ratio >= 0.8:
            strategy = "primary_replica"
            topology = "1 primary + N read replicas"
            nodes = [
                {"role": "primary", "purpose": "write traffic"},
                {"role": "replica", "purpose": "read traffic", "count": max(2, qps // 1000)},
            ]
            failover = "automatic (Patroni or similar)"
            lag_ms = 50
        elif read_ratio >= 0.5:
            strategy = "primary_replica"
            topology = "1 primary + 1-2 read replicas"
            nodes = [
                {"role": "primary", "purpose": "write traffic"},
                {"role": "replica", "purpose": "read traffic + failover", "count": 2},
            ]
            failover = "automatic with manual promotion"
            lag_ms = 100
        elif data_gb > 100:
            strategy = "multi_primary"
            topology = "N primary nodes (multi-region)"
            nodes = [
                {"role": "primary", "purpose": "regional write", "count": 3},
            ]
            failover = "automatic (conflict resolution enabled)"
            lag_ms = 200
        else:
            strategy = "primary_replica"
            topology = "1 primary + 1 replica (HA)"
            nodes = [
                {"role": "primary", "purpose": "write traffic"},
                {"role": "replica", "purpose": "failover", "count": 1},
            ]
            failover = "manual promotion"
            lag_ms = 50

        return ReplicationDesign(
            strategy=strategy,
            topology=topology,
            nodes=nodes,
            failover_strategy=failover,
            estimated_lag_ms=lag_ms,
        )

    def _default_design(self, database_type: DatabaseType) -> ReplicationDesign:
        """Return a default replication design."""
        return ReplicationDesign(
            strategy="primary_replica",
            topology="1 primary + 1 replica (standard HA)",
            nodes=[
                {"role": "primary", "purpose": "write traffic"},
                {"role": "replica", "purpose": "failover", "count": 1},
            ],
            failover_strategy="manual promotion",
            estimated_lag_ms=100,
        )
