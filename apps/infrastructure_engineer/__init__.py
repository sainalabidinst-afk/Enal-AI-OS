"""
Infrastructure Engineer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.infrastructure_engineer.engine import InfrastructureEngineerEngine
from apps.infrastructure_engineer.worker import InfrastructureEngineerWorker
from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    InfrastructureEngineerReport,
    OperationType,
    InfrastructureType,
    HighAvailabilityMode,
    StorageType,
    StorageTier,
    DisasterRecoveryStrategy,
    BackupSchedule,
    ComputeResource,
    NetworkConfig,
    KubernetesSpec,
    ClusterSpec,
    NodeConfig,
    FailoverConfig,
    VolumeSpec,
    StorageClassSpec,
    DRPlan,
    RecoveryPointObjective,
    RecoveryTimeObjective,
    BusinessContext,
    QualityAttributes,
    InfrastructureRecord,
)


class InfrastructureEngineerApp(BaseReferenceApp):
    name = "infrastructure-engineer"
    version = "1.0.0"
    description = "Infrastructure design, availability, and disaster recovery planning"
    category = "infrastructure"
    pipeline = ["perception", "analysis", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = InfrastructureEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> InfrastructureEngineerApp:
    return InfrastructureEngineerApp()

__all__ = [
    "InfrastructureEngineerApp",
    "get_app",
    "InfrastructureEngineerEngine",
    "InfrastructureEngineerWorker",
    "InfrastructureEngineerRequest",
    "InfrastructureEngineerReport",
    "OperationType",
    "InfrastructureType",
    "HighAvailabilityMode",
    "StorageType",
    "StorageTier",
    "DisasterRecoveryStrategy",
    "BackupSchedule",
    "ComputeResource",
    "NetworkConfig",
    "KubernetesSpec",
    "ClusterSpec",
    "NodeConfig",
    "FailoverConfig",
    "VolumeSpec",
    "StorageClassSpec",
    "DRPlan",
    "RecoveryPointObjective",
    "RecoveryTimeObjective",
    "BusinessContext",
    "QualityAttributes",
    "InfrastructureRecord",
]
