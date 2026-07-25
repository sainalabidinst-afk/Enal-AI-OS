"""
Audit Trail
===========

Records all deployment steps as artifacts.
Deployment → Backup → Diff → Approval → Execution → Verification → Rollback → Final Report
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AuditEventType(str, Enum):
    DEPLOYMENT_START = "deployment_start"
    BACKUP = "backup"
    DIFF = "diff"
    RISK_SCORE = "risk_score"
    HUMAN_APPROVAL = "human_approval"
    DEPLOY = "deploy"
    VERIFICATION = "verification"
    ROLLBACK = "rollback"
    FINAL_REPORT = "final_report"


@dataclass
class AuditEvent:
    event_type: AuditEventType
    timestamp: str
    actor: str
    details: dict[str, Any] = field(default_factory=dict)
    artifact_id: str | None = None


@dataclass
class AuditTrail:
    deployment_id: str
    events: list[AuditEvent] = field(default_factory=list)

    def add_event(self, event_type: AuditEventType, actor: str, details: dict[str, Any] | None = None, artifact_id: str | None = None):
        event = AuditEvent(
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            actor=actor,
            details=details or {},
            artifact_id=artifact_id,
        )
        self.events.append(event)
        return event

    def to_markdown(self) -> str:
        lines = [f"# Audit Trail — Deployment {self.deployment_id}\n"]
        for i, event in enumerate(self.events, 1):
            lines.append(f"## {i}. {event.event_type.value.replace('_', ' ').title()}")
            lines.append(f"- **Timestamp**: {event.timestamp}")
            lines.append(f"- **Actor**: {event.actor}")
            if event.artifact_id:
                lines.append(f"- **Artifact**: {event.artifact_id}")
            if event.details:
                lines.append(f"- **Details**: {event.details}")
            lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "deployment_id": self.deployment_id,
            "events": [
                {
                    "event_type": e.event_type.value,
                    "timestamp": e.timestamp,
                    "actor": e.actor,
                    "details": e.details,
                    "artifact_id": e.artifact_id,
                }
                for e in self.events
            ],
        }


class AuditTrailManager:
    """Manages audit trails for deployments."""

    def __init__(self):
        self._trails: dict[str, AuditTrail] = {}

    def create_trail(self, deployment_id: str) -> AuditTrail:
        """Create a new audit trail."""
        trail = AuditTrail(deployment_id=deployment_id)
        self._trails[deployment_id] = trail
        return trail

    def get_trail(self, deployment_id: str) -> AuditTrail | None:
        """Get an audit trail by deployment ID."""
        return self._trails.get(deployment_id)

    def generate_report(self, deployment_id: str) -> str:
        """Generate audit report for a deployment."""
        trail = self._trails.get(deployment_id)
        if not trail:
            return f"No audit trail found for {deployment_id}"
        return trail.to_markdown()


audit_trail_manager = AuditTrailManager()
