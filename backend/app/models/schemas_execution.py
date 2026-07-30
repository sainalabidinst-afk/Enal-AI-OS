from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    pending = "pending"
    planning = "planning"
    running = "running"
    waiting_approval = "waiting_approval"
    paused = "paused"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class ExecutionTask(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    name: str
    status: ExecutionStatus = ExecutionStatus.pending
    progress: float = 0.0
    dependencies: list[str] = []
    result: dict[str, Any] | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class ExecutionGraph(BaseModel):
    tasks: dict[str, ExecutionTask] = {}
    edges: list[dict[str, str]] = []
    entry_point: str | None = None


class ExecutionPhase(BaseModel):
    id: str
    name: str
    status: ExecutionStatus
    progress: float = 0.0
    tasks: list[dict[str, Any]] = []
    started_at: datetime | None = None
    completed_at: datetime | None = None


class ExecutionSession(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    goal: str
    status: ExecutionStatus = ExecutionStatus.pending
    progress: float = 0.0
    eta_seconds: int | None = None
    phases: list[dict[str, Any]] = []
    artifacts: list[str] = []
    logs: list[dict[str, Any]] = []
    workspace_id: str | None = None
    conversation_id: str | None = None
    graph: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None


class ExecutionArtifact(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    execution_id: str
    name: str
    type: str
    content: str | None = None
    path: str | None = None
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = {}


class Workspace(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    name: str
    description: str | None = None
    conversation_ids: list[str] = []
    execution_ids: list[str] = []
    artifact_ids: list[str] = []
    files: list[dict[str, Any]] = []
    memory: dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ArtifactVersion(BaseModel):
    version: int
    created_at: datetime
    content: str | None = None
    path: str | None = None
    metadata: dict[str, Any] = {}


class Artifact(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    workspace_id: str
    name: str
    type: str
    description: str | None = None
    current_version: int = 1
    versions: list[ArtifactVersion] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
