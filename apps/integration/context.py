"""
Shared Capability Context
==========================

Provides a single mutable context object that flows through
the entire integration workflow.

This allows capabilities to collaborate without direct references
to each other. They read/write to the shared context instead.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from apps.integration.evidence_adapter import UnifiedEvidence

logger = logging.getLogger(__name__)


@dataclass
class CapabilityContext:
    """
    Shared context passed through an integration workflow.

    Stages may read inputs from here, write intermediate results,
    and produce final outputs. Nothing outside the workflow needs
    to know about internal handoffs.
    """

    workflow_id: str = field(default_factory=lambda: f"ctx_{uuid.uuid4().hex[:8]}")
    workflow_type: str | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    evidences: list[UnifiedEvidence] = field(default_factory=list)
    intermediate: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None

    def set_input(self, key: str, value: Any) -> CapabilityContext:
        self.inputs[key] = value
        return self

    def get_input(self, key: str, default: Any = None) -> Any:
        return self.inputs.get(key, default)

    def add_evidence(self, evidence: UnifiedEvidence) -> CapabilityContext:
        self.evidences.append(evidence)
        return self

    def add_evidences(self, evidences: list[UnifiedEvidence]) -> CapabilityContext:
        self.evidences.extend(evidences)
        return self

    def set_intermediate(self, key: str, value: Any) -> CapabilityContext:
        self.intermediate[key] = value
        return self

    def get_intermediate(self, key: str, default: Any = None) -> Any:
        return self.intermediate.get(key, default)

    def set_output(self, key: str, value: Any) -> CapabilityContext:
        self.outputs[key] = value
        return self

    def get_output(self, key: str, default: Any = None) -> Any:
        return self.outputs.get(key, default)

    def set_metadata(self, key: str, value: Any) -> CapabilityContext:
        self.metadata[key] = value
        return self

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def mark_completed(self) -> CapabilityContext:
        self.completed_at = datetime.now(timezone.utc).isoformat()
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "inputs": dict(self.inputs),
            "evidences": [e.to_dict() for e in self.evidences],
            "intermediate": dict(self.intermediate),
            "outputs": dict(self.outputs),
            "metadata": dict(self.metadata),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
