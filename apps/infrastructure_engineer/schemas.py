"""
Infrastructure Engineer Schemas
=================================

Typed contracts for the Infrastructure Engineer capability pack.
Defines the input (InfrastructureEngineerRequest) and output
(InfrastructureEngineerReport) contracts, plus all supporting types.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    kubernetes_design = "kubernetes_design"
    ha_cluster_design = "ha_cluster_design"
    storage_design = "storage_design"
    disaster_recovery_plan = "disaster_recovery_plan"
    infrastructure_assessment = "infrastructure_assessment"


class InfrastructureType(str, Enum):
    kubernetes = "kubernetes"
    ha_cluster = "ha_cluster"
    storage = "storage"
    disaster_recovery = "disaster_recovery"
    hybrid = "hybrid"


class HighAvailabilityMode(str, Enum):
    active_passive = "active_passive"
    active_active = "active_active"
    active_standby = "active_standby"
    n_plus_1 = "n_plus_1"


class StorageType(str, Enum):
    block = "block"
    file = "file"
    object = "object"
    distributed = "distributed"


class StorageTier(str, Enum):
    hot = "hot"
    warm = "warm"
    cold = "cold"
    archive = "archive"


class DisasterRecoveryStrategy(str, Enum):
    backup_restore = "backup_restore"
    pilot_light = "pilot_light"
    warm_standby = "warm_standby"
    multi_site_active_active = "multi_site_active_active"


class OutputFormat(str, Enum):
    yaml = "yaml"
    json = "json"
    markdown = "markdown"
    terraform = "terraform"
    helm = "helm"


class BusinessContext(BaseModel):
    domain: str = Field(default="", description="Business domain (e-commerce, fintech, etc.)")
    project_name: str = Field(default="", description="Project name")
    description: str = Field(default="", description="Project overview")


class QualityAttributes(BaseModel):
    availability_target: str = Field(default="99.9%", description="Target availability SLA")
    performance_target: str = Field(default="< 200ms", description="Performance target")
    durability_target: str = Field(default="99.999999999%", description="Storage durability target")
    security_target: str = Field(default="OWASP + CIS benchmarks", description="Security baseline")


class ComputeResource(BaseModel):
    cpu_cores: int = Field(default=2, description="Number of CPU cores")
    memory_gb: int = Field(default=4, description="Memory in GB")
    disk_gb: int = Field(default=40, description="Disk in GB")
    gpu_count: int = Field(default=0, description="Number of GPUs")


class NetworkConfig(BaseModel):
    cidr: str = Field(default="10.0.0.0/16", description="Network CIDR block")
    subnet_count: int = Field(default=3, description="Number of subnets")
    load_balancer_type: str = Field(default="layer4", description="Load balancer type")
    ingress_controller: str = Field(default="nginx", description="Ingress controller")
    dns_policy: str = Field(default="cluster_first", description="DNS policy")


class NodeConfig(BaseModel):
    count: int = Field(default=3, description="Number of nodes")
    instance_type: str = Field(default="t3.medium", description="Cloud instance type")
    os_image: str = Field(default="ubuntu-22.04", description="Node OS image")
    labels: dict[str, str] = Field(default_factory=dict, description="Node labels")
    taints: list[str] = Field(default_factory=list, description="Node taints")


class KubernetesSpec(BaseModel):
    cluster_name: str = Field(default="", description="Cluster name")
    kubernetes_version: str = Field(default="1.28", description="Kubernetes version")
    network_policy: bool = Field(default=True, description="Enable network policies")
    rbac_enabled: bool = Field(default=True, description="Enable RBAC")
    pod_security_standard: str = Field(default="restricted", description="Pod security standard")
    resource_quotas: bool = Field(default=True, description="Enable resource quotas")
    limit_ranges: bool = Field(default=True, description="Enable limit ranges")
    nodes: list[NodeConfig] = Field(default_factory=list, description="Node configurations")
    network: NetworkConfig = Field(default_factory=NetworkConfig, description="Network configuration")


class FailoverConfig(BaseModel):
    mode: HighAvailabilityMode = Field(default=HighAvailabilityMode.active_passive)
    heartbeat_interval_seconds: int = Field(default=5, description="Heartbeat interval")
    failover_timeout_seconds: int = Field(default=30, description="Failover timeout")
    quorum_required: bool = Field(default=True, description="Require quorum for failover")
    fencing_mechanism: str = Field(default="stonith", description="Fencing mechanism (STONITH)")


class ClusterSpec(BaseModel):
    cluster_name: str = Field(default="", description="Cluster name")
    nodes: list[NodeConfig] = Field(default_factory=list, description="Node configurations")
    ha_mode: HighAvailabilityMode = Field(default=HighAvailabilityMode.active_passive)
    shared_storage: str = Field(default="", description="Shared storage type")
    failover: FailoverConfig = Field(default_factory=FailoverConfig, description="Failover configuration")
    load_balancer: str = Field(default="haproxy", description="Load balancer type")


class VolumeSpec(BaseModel):
    name: str = Field(default="", description="Volume name")
    size_gb: int = Field(default=100, description="Volume size in GB")
    storage_type: StorageType = Field(default=StorageType.block)
    storage_tier: StorageTier = Field(default=StorageTier.hot)
    iops: int = Field(default=3000, description="IOPS for block storage")
    throughput_mbps: int = Field(default=125, description="Throughput in Mbps")
    replicas: int = Field(default=3, description="Number of replicas")
    encryption: bool = Field(default=True, description="Enable encryption at rest")
    snapshot_enabled: bool = Field(default=True, description="Enable snapshots")


class StorageClassSpec(BaseModel):
    name: str = Field(default="", description="Storage class name")
    storage_type: StorageType = Field(default=StorageType.block)
    storage_tier: StorageTier = Field(default=StorageTier.hot)
    reclaim_policy: str = Field(default="retain", description="Reclaim policy")
    volume_expansion: bool = Field(default=True, description="Allow volume expansion")
    allowed_topologies: list[str] = Field(default_factory=list, description="Allowed topology keys")


class BackupSchedule(BaseModel):
    frequency: str = Field(default="daily", description="Backup frequency (hourly, daily, weekly)")
    retention_days: int = Field(default=30, description="Retention period in days")
    backup_type: str = Field(default="full", description="Backup type (full, incremental, differential)")
    encryption: bool = Field(default=True, description="Encrypt backups")
    compression: bool = Field(default=True, description="Compress backups")


class RecoveryPointObjective(BaseModel):
    rpo_minutes: int = Field(default=60, description="Maximum acceptable data loss in minutes")
    rto_minutes: int = Field(default=240, description="Maximum acceptable downtime in minutes")


class RecoveryTimeObjective(BaseModel):
    recovery_time_minutes: int = Field(default=240, description="Target recovery time in minutes")
    data_loss_tolerance_minutes: int = Field(default=60, description="Maximum acceptable data loss")


class DRPlan(BaseModel):
    strategy: DisasterRecoveryStrategy = Field(default=DisasterRecoveryStrategy.warm_standby)
    primary_region: str = Field(default="us-east-1", description="Primary region")
    secondary_region: str = Field(default="us-west-2", description="Secondary/DR region")
    rpo: RecoveryPointObjective = Field(default_factory=RecoveryPointObjective, description="RPO/RTO targets")
    backup_schedule: BackupSchedule = Field(default_factory=BackupSchedule, description="Backup schedule")
    failover_runbook: str = Field(default="", description="Failover runbook reference")
    testing_schedule: str = Field(default="quarterly", description="DR testing schedule")
    communication_plan: list[str] = Field(default_factory=list, description="Communication plan steps")


class InfrastructureEngineerRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(default=OperationType.kubernetes_design)
    business_context: BusinessContext = Field(default_factory=BusinessContext)
    quality_attributes: QualityAttributes = Field(default_factory=QualityAttributes)
    infrastructure_type: InfrastructureType = Field(default=InfrastructureType.kubernetes)
    output_format: OutputFormat = Field(default=OutputFormat.yaml)
    inputs: dict[str, Any] = Field(default_factory=dict, description="Operation-specific inputs")


class InfrastructureEngineerReport(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = Field(default="")
    kubernetes_spec: KubernetesSpec | None = Field(default=None, description="Kubernetes design")
    cluster_spec: ClusterSpec | None = Field(default=None, description="HA cluster design")
    storage_specs: list[VolumeSpec | StorageClassSpec] = Field(default_factory=list, description="Storage specs")
    dr_plan: DRPlan | None = Field(default=None, description="Disaster recovery plan")
    cost_estimate: dict[str, float] = Field(default_factory=dict, description="Cost estimate by component")
    security_hardening: list[str] = Field(default_factory=list, description="Security hardening measures")
    compliance_status: dict[str, bool] = Field(default_factory=dict, description="Compliance checklist")
    recommendations: list[str] = Field(default_factory=list, description="Improvement recommendations")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall quality score")
    explanation: str = Field(default="", description="Human-readable analysis summary")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        data = self.model_dump()
        data["generated_at"] = self.generated_at.isoformat()
        return data


class InfrastructureRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(default="")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    operation: str = Field(default="")
    infrastructure_type: str = Field(default="")
    availability_achieved: str = Field(default="")
    rpo_achieved_minutes: int = Field(default=0)
    rto_achieved_minutes: int = Field(default=0)
    cost_monthly_usd: float = Field(default=0.0)
    compliance_passed: bool = Field(default=True)
    outcome: str = Field(default="accepted", description="accepted | partially_accepted | rejected | revised")
