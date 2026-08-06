"""
Add observability modules to capabilities that are missing them.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPS_DIR = ROOT / "apps"

CAPABILITIES_NEEDING_OBSERVABILITY = [
    "ai_engineer",
    "business_analyst",
    "code_engineer",
    "data_engineer",
    "database_engineer",
    "devops_assistant",
    "documentation_engineer",
    "full_stack_engineer",
    "integration",
    "qa_engineer",
    "research_assistant",
    "security_engineer",
    "self_development",
    "society",
    "system_architect",
    "ui_ux_designer",
]


def add_observability(capability_id: str) -> None:
    app_dir = APPS_DIR / capability_id
    log_file = app_dir / "observability_log.py"
    metric_file = app_dir / "observability_metrics.py"

    if log_file.exists() or metric_file.exists():
        return

    name = capability_id.replace("_", " ").title()

    log_content = f'''"""
Observability log for {name}.
"""

import logging

logger = logging.getLogger(__name__)


def log_execution(capability_id: str, operation: str, duration_ms: float) -> None:
    """Log capability execution."""
    logger.info("Capability %s executed %s in %.2fms", capability_id, operation, duration_ms)


def log_error(capability_id: str, operation: str, error: Exception) -> None:
    """Log capability error."""
    logger.error("Capability %s failed %s: %s", capability_id, operation, error)
'''

    metric_content = f'''"""
Observability metrics for {name}.
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


metrics_store: dict[str, CapabilityMetrics] = {{}}


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
'''

    log_file.write_text(log_content, encoding="utf-8")
    metric_file.write_text(metric_content, encoding="utf-8")
    print(f"Added observability to {capability_id}")


def main() -> int:
    for capability in CAPABILITIES_NEEDING_OBSERVABILITY:
        add_observability(capability)
    print(f"\nAdded observability modules to {len(CAPABILITIES_NEEDING_OBSERVABILITY)} capabilities.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
