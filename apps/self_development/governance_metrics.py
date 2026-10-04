"""
Governance Metrics
==================

Tracks Pilar 4 governance metrics:
- Pack synthesis acceptance rate
- Remediation success rate
- Federated sync privacy violation rate
- Governance gate latency
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class GovernanceMetrics:
    pack_synthesis_attempts: int = 0
    pack_synthesis_accepted: int = 0
    remediation_attempts: int = 0
    remediation_successes: int = 0
    federated_syncs: int = 0
    federated_privacy_violations: int = 0
    gate_latencies_ms: list[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def pack_synthesis_acceptance_rate(self) -> float:
        if self.pack_synthesis_attempts == 0:
            return 0.0
        return self.pack_synthesis_accepted / self.pack_synthesis_attempts

    @property
    def remediation_success_rate(self) -> float:
        if self.remediation_attempts == 0:
            return 0.0
        return self.remediation_successes / self.remediation_attempts

    @property
    def federated_privacy_violation_rate(self) -> float:
        if self.federated_syncs == 0:
            return 0.0
        return self.federated_privacy_violations / self.federated_syncs

    @property
    def avg_gate_latency_ms(self) -> float:
        if not self.gate_latencies_ms:
            return 0.0
        return sum(self.gate_latencies_ms) / len(self.gate_latencies_ms)

    def record_pack_synthesis(self, accepted: bool) -> None:
        self.pack_synthesis_attempts += 1
        if accepted:
            self.pack_synthesis_accepted += 1
        self.updated_at = datetime.now(UTC)

    def record_remediation(self, success: bool) -> None:
        self.remediation_attempts += 1
        if success:
            self.remediation_successes += 1
        self.updated_at = datetime.now(UTC)

    def record_federated_sync(self, pii_removed: bool) -> None:
        self.federated_syncs += 1
        if not pii_removed:
            self.federated_privacy_violations += 1
        self.updated_at = datetime.now(UTC)

    def record_gate_latency(self, latency_ms: float) -> None:
        self.gate_latencies_ms.append(latency_ms)
        self.updated_at = datetime.now(UTC)

    def snapshot(self) -> dict[str, Any]:
        return {
            "pack_synthesis_acceptance_rate": round(self.pack_synthesis_acceptance_rate, 4),
            "remediation_success_rate": round(self.remediation_success_rate, 4),
            "federated_privacy_violation_rate": round(self.federated_privacy_violation_rate, 4),
            "avg_gate_latency_ms": round(self.avg_gate_latency_ms, 2),
            "pack_synthesis_attempts": self.pack_synthesis_attempts,
            "pack_synthesis_accepted": self.pack_synthesis_accepted,
            "remediation_attempts": self.remediation_attempts,
            "remediation_successes": self.remediation_successes,
            "federated_syncs": self.federated_syncs,
            "federated_privacy_violations": self.federated_privacy_violations,
            "updated_at": self.updated_at.isoformat(),
        }


governance_metrics = GovernanceMetrics()
