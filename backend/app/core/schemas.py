"""
Pydantic schemas for the RFC-0001 Stable Contract.

Defines typed models for:
  - Task/Intent input contract
  - Task Result output contract
  - Event Bus typed events
  - skills.yaml manifest schema
  - Contract version info
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------


class ContractVersion(BaseModel):
    """Semantic version for stable contract API."""

    model_config = ConfigDict(frozen=True)

    MAJOR: int = 1
    MINOR: int = 0
    PATCH: int = 0

    @property
    def VERSION(self) -> str:  # noqa: N802 — RFC-0001 contract property name
        """Return version as a semver string."""
        return f"{self.MAJOR}.{self.MINOR}.{self.PATCH}"

    def is_backward_compatible(self, other: ContractVersion) -> bool:
        if self.MAJOR != other.MAJOR:
            return False
        return self.MINOR >= other.MINOR

    @classmethod
    def parse(cls, version_str: str) -> ContractVersion:
        parts = version_str.strip().lstrip("v").split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return cls(MAJOR=major, MINOR=minor, PATCH=patch)


CONTRACT_VERSION = ContractVersion()


# ---------------------------------------------------------------------------
# Task / Intent contracts
# ---------------------------------------------------------------------------

TaskPriority = Literal["low", "normal", "high", "critical"]
TaskStatus = Literal["success", "failure", "timeout", "partial"]
OutputType = Literal["code", "config", "report", "analysis", "recommendation"]


class TaskContext(BaseModel):
    """Context payload for a task / intent request."""

    model_config = ConfigDict(extra="allow")

    workspace_path: str | None = None
    language: str | None = None
    framework: str | None = None
    user_input: str = ""


class TaskMetadata(BaseModel):
    """Tracing metadata attached to every task."""

    model_config = ConfigDict(extra="allow")

    source: str = "system"
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class TaskIntentRequest(BaseModel):
    """Incoming Task/Intent contract (RFC-0001 § Kontrak Masukan)."""

    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    intent: str
    context: TaskContext = Field(default_factory=TaskContext)
    capabilities_required: list[str] = Field(default_factory=list)
    priority: TaskPriority = "normal"
    timeout_ms: int = 30000
    metadata: TaskMetadata = Field(default_factory=TaskMetadata)


class TaskResultMetrics(BaseModel):
    model_config = ConfigDict(extra="allow")

    latency_ms: float = 0.0
    tokens_used: int = 0
    memory_mb: float = 0.0


class TaskError(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: str = ""
    message: str = ""
    recoverable: bool = True


class EmittedEvent(BaseModel):
    model_config = ConfigDict(extra="allow")

    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class TaskResultPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    output_type: OutputType = "analysis"
    payload: dict[str, Any] = Field(default_factory=dict)
    artifacts: list[str] = Field(default_factory=list)
    confidence_score: float = 0.0


class TaskResult(BaseModel):
    """Outgoing Task Result contract (RFC-0001 § Kontrak Keluaran)."""

    task_id: str
    intent: str
    status: TaskStatus = "success"
    result: TaskResultPayload = Field(default_factory=TaskResultPayload)
    events_emitted: list[EmittedEvent] = Field(default_factory=list)
    metrics: TaskResultMetrics = Field(default_factory=TaskResultMetrics)
    error: TaskError | None = None


# ---------------------------------------------------------------------------
# Event Bus typed events
# ---------------------------------------------------------------------------


class EventPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class Event(BaseModel):
    """Typed event for the RFC-0001 Event Bus (Pydantic-validated)."""

    model_config = ConfigDict(extra="allow", frozen=False)

    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    source: str = "system"
    target: str = "*"
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    correlation_id: str | None = None
    trace_id: str | None = None
    priority: EventPriority = EventPriority.NORMAL
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        extra="allow",
        frozen=False,
        json_encoders={datetime: lambda v: v.isoformat()},
    )


class EventEnvelope(BaseModel):
    """Envelope wrapping an event with delivery metadata."""

    event: Event
    stream: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    delivered: bool = False
    delivered_at: str | None = None


# ---------------------------------------------------------------------------
# skills.yaml manifest schema
# ---------------------------------------------------------------------------


class CapabilityEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    description: str
    input_schema: str = ""
    output_schema: str = ""


class ExternalDependency(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    version: str


class DependencySpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    capabilities: list[str] = Field(default_factory=list)
    external: list[ExternalDependency] = Field(default_factory=list)


class PipelineStage(BaseModel):
    model_config = ConfigDict(extra="allow")

    stage: str
    capability: str


class CapabilityPackManifest(BaseModel):
    """Pydantic model for the RFC-0001 skills.yaml manifest."""

    model_config = ConfigDict(extra="allow")

    capability_pack: CapabilityPackConfig


class CapabilityPackConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    version: str = "1.0.0"
    display_name: str = ""
    description: str = ""
    entry_point: str = ""
    category: str = ""
    maturity_level: int = 1
    quality_target: str = "A"
    capabilities: list[CapabilityEntry] = Field(default_factory=list)
    dependencies: DependencySpec = Field(default_factory=DependencySpec)
    pipeline: list[PipelineStage] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


CapabilityPackManifest.model_rebuild()


# ---------------------------------------------------------------------------
# Contract compliance report
# ---------------------------------------------------------------------------


class ComplianceReport(BaseModel):
    model_config = ConfigDict(extra="allow")

    pack_id: str
    version: str
    passes: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    methods_implemented: list[str] = Field(default_factory=list)
    methods_expected: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Blueprint schemas for visual builder
# ---------------------------------------------------------------------------


class ToolStep(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    type: str
    label: str = ""
    config: dict[str, Any] = Field(default_factory=dict)


class ConditionalBranch(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    label: str = ""
    condition: str = ""
    steps: list[ToolStep] = Field(default_factory=list)


class AgentBlueprint(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    model: str = "gpt-4o"
    tools: list[str] = Field(default_factory=list)
    knowledge_base_ids: list[str] = Field(default_factory=list)
    prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 1024
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolBlueprint(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    steps: list[ToolStep] = Field(default_factory=list)
    branches: list[ConditionalBranch] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    # Version
    "ContractVersion",
    "CONTRACT_VERSION",
    # Task contracts
    "TaskContext",
    "TaskMetadata",
    "TaskIntentRequest",
    "TaskResult",
    "TaskResultPayload",
    "TaskResultMetrics",
    "TaskError",
    "EmittedEvent",
    "TaskPriority",
    "TaskStatus",
    "OutputType",
    # Event Bus
    "Event",
    "EventEnvelope",
    "EventPriority",
    # skills.yaml
    "CapabilityPackManifest",
    "CapabilityPackConfig",
    "CapabilityEntry",
    "DependencySpec",
    "ExternalDependency",
    "PipelineStage",
    # Reports
    "ComplianceReport",
    # Blueprints
    "AgentBlueprint",
    "ToolBlueprint",
    "ToolStep",
    "ConditionalBranch",
]
