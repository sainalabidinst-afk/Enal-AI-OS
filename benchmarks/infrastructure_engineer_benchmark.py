"""
Infrastructure Engineer Benchmark
====================================

Benchmark scenarios for validating Infrastructure Engineer capability pack.
Target: A (≥90%) with 10 scenarios across 6 dimensions.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "infra-001",
        "name": "Kubernetes Microservice Deployment",
        "category": "kubernetes",
        "inputs": {
            "business_context": {"project_name": "microservice-app", "domain": "e-commerce"},
            "inputs": {"node_count": 3, "kubernetes_version": "1.28"},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "infra-002",
        "name": "HA Cluster PostgreSQL",
        "category": "ha_cluster",
        "inputs": {
            "business_context": {"project_name": "postgres-ha", "domain": "fintech"},
            "inputs": {"node_count": 3, "availability_target": "99.99%"},
            "quality_attributes": {"availability_target": "99.99%"},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "infra-003",
        "name": "Disaster Recovery Plan",
        "category": "disaster_recovery",
        "inputs": {
            "business_context": {"project_name": "dr-plan", "domain": "healthcare"},
            "inputs": {"rpo_minutes": 15, "rto_minutes": 30},
            "quality_attributes": {"availability_target": "99.99%"},
        },
        "min_quality_score": 0.85,
    },
    {
        "id": "infra-004",
        "name": "Storage Design untuk Database",
        "category": "storage",
        "inputs": {
            "business_context": {"project_name": "db-storage", "domain": "fintech"},
            "inputs": {"storage_specs": [{"name": "db-ssd", "size_gb": 500, "iops": 10000, "storage_type": "ssd"}]},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "infra-005",
        "name": "Load Balancer Configuration",
        "category": "load_balancer",
        "inputs": {
            "business_context": {"project_name": "lb-config", "domain": "e-commerce"},
            "inputs": {"lb_type": "haproxy", "backend_count": 5},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "infra-006",
        "name": "Proxmox Virtual Environment",
        "category": "proxmox",
        "inputs": {
            "business_context": {"project_name": "proxmox-cluster", "domain": "enterprise"},
            "inputs": {"node_count": 3, "vm_count": 20},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "infra-007",
        "name": "Ceph Distributed Storage",
        "category": "storage",
        "inputs": {
            "business_context": {"project_name": "ceph-cluster", "domain": "enterprise"},
            "inputs": {"osd_count": 12, "replication_factor": 3},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "infra-008",
        "name": "Docker Swarm Multi-Host",
        "category": "docker_swarm",
        "inputs": {
            "business_context": {"project_name": "swarm-cluster", "domain": "saas"},
            "inputs": {"manager_count": 3, "worker_count": 5},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "infra-009",
        "name": "VMware vSphere Design",
        "category": "vmware",
        "inputs": {
            "business_context": {"project_name": "vsphere-cluster", "domain": "enterprise"},
            "inputs": {"esxi_count": 4, "vm_count": 50},
            "quality_attributes": {"availability_target": "99.9%"},
        },
        "min_quality_score": 0.80,
    },
    {
        "id": "infra-010",
        "name": "Multi-Region DR dengan RPO/RTO",
        "category": "disaster_recovery",
        "inputs": {
            "business_context": {"project_name": "multi-region-dr", "domain": "fintech"},
            "inputs": {"primary_region": "us-east-1", "secondary_region": "eu-west-1", "rpo_minutes": 5, "rto_minutes": 15},
            "quality_attributes": {"availability_target": "99.99%"},
        },
        "min_quality_score": 0.85,
    },
]


def get_scenarios() -> list[dict[str, Any]]:
    return SCENARIOS


def get_scenario_by_id(scenario_id: str) -> dict[str, Any] | None:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None
