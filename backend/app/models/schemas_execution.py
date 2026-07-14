from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


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
    dependencies: List[str] = []
    result: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ExecutionGraph(BaseModel):
    tasks: Dict[str, ExecutionTask] = {}
    edges: List[Dict[str, str]] = []
    entry_point: Optional[str] = None


class ExecutionPhase(BaseModel):
    id: str
    name: str
    status: ExecutionStatus
    progress: float = 0.0
    tasks: List[Dict[str, Any]] = []
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ExecutionSession(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    goal: str
    status: ExecutionStatus = ExecutionStatus.pending
    progress: float = 0.0
    eta_seconds: Optional[int] = None
    phases: List[Dict[str, Any]] = []
    artifacts: List[str] = []
    logs: List[Dict[str, Any]] = []
    workspace_id: Optional[str] = None
    conversation_id: Optional[str] = None
    graph: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None


class ExecutionArtifact(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    execution_id: str
    name: str
    type: str
    content: Optional[str] = None
    path: Optional[str] = None
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = {}


class Workspace(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    name: str
    description: Optional[str] = None
    conversation_ids: List[str] = []
    execution_ids: List[str] = []
    artifact_ids: List[str] = []
    files: List[Dict[str, Any]] = []
    memory: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ArtifactVersion(BaseModel):
    version: int
    created_at: datetime
    content: Optional[str] = None
    path: Optional[str] = None
    metadata: Dict[str, Any] = {}


class Artifact(BaseModel):
    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex)
    workspace_id: str
    name: str
    type: str
    description: Optional[str] = None
    current_version: int = 1
    versions: List[ArtifactVersion] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
