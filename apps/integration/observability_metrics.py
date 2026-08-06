"""
Observability metrics for Integration.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CapabilityMetrics:
    capability_id: str
    execution_count: int = 0
    success_count: int = 0
    error_count: int = 0
    total_duration_ms: float = 0.0
    last_executed_at: str = ""

    @property
    def success_rate(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return (self.success_count / self.execution_count) * 100

    @property
    def average_duration_ms(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return self.total_duration_ms / self.execution_count


metrics_store: dict[str, CapabilityMetrics] = {}


def get_metrics(capability_id: str) -> CapabilityMetrics:
    if capability_id not in metrics_store:
        metrics_store[capability_id] = CapabilityMetrics(capability_id=capability_id)
    return metrics_store[capability_id]


def record_execution(capability_id: str, duration_ms: float, success: bool = True) -> None:
    metrics = get_metrics(capability_id)
    metrics.execution_count += 1
    if success:
        metrics.success_count += 1
    else:
        metrics.error_count += 1
    metrics.total_duration_ms += duration_ms
