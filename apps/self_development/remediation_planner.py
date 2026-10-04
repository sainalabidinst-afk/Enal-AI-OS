"""
Remediation Planner
===================

Generates remediation playbooks from anomalies and routes high-risk actions
through the consent gate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from apps.self_development.anomaly_detector import Anomaly

logger = logging.getLogger(__name__)


@dataclass
class RemediationPlaybook:
    playbook_id: str
    anomaly_id: str
    title: str
    steps: list[str]
    severity: str
    requires_consent: bool
    status: str = "pending"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class RemediationPlanner:
    """Plans remediation playbooks for anomalies."""

    def __init__(self, consent_gate: Any | None = None) -> None:
        self.consent_gate = consent_gate

    def plan(self, anomaly: Anomaly) -> RemediationPlaybook:
        steps = self._build_steps(anomaly)
        requires_consent = anomaly.severity in {"high", "critical"}
        playbook = RemediationPlaybook(
            playbook_id=f"playbook-{anomaly.anomaly_id}",
            anomaly_id=anomaly.anomaly_id,
            title=f"Remediate {anomaly.metric} anomaly",
            steps=steps,
            severity=anomaly.severity,
            requires_consent=requires_consent,
        )
        if requires_consent and self.consent_gate is not None:
            self.consent_gate.request(anomaly=anomaly, playbook=playbook)
        return playbook

    def _build_steps(self, anomaly: Anomaly) -> list[str]:
        category = anomaly.category
        if category == "performance":
            return [
                "Review current resource utilization",
                "Scale or optimize affected component",
                "Validate improvement after remediation",
            ]
        if category == "security":
            return [
                "Isolate affected component",
                "Apply security patch or configuration change",
                "Run validation tests",
            ]
        if category == "infrastructure":
            return [
                "Check component health",
                "Restart or redeploy if necessary",
                "Verify service recovery",
            ]
        return [
            "Investigate anomaly root cause",
            "Apply remediation",
            "Validate outcome",
        ]


class RemediationConsentGate:
    """Consent gate adapter for remediation."""

    def __init__(self, consent_manager: Any | None = None) -> None:
        try:
            from backend.app.core.consent import consent_manager
            self.consent_manager = consent_manager
        except Exception:
            self.consent_manager = consent_manager

    def request(self, anomaly: Anomaly, playbook: RemediationPlaybook) -> str | None:
        if self.consent_manager is None:
            logger.warning("Consent manager not available; skipping consent request")
            return None
        request = self.consent_manager.request(
            action_type=f"remediation.{playbook.playbook_id}",
            description=playbook.title,
            params={
                "anomaly_id": anomaly.anomaly_id,
                "severity": anomaly.severity,
                "metric": anomaly.metric,
                "deviation_pct": anomaly.deviation_pct,
            },
        )
        return request.request_id
