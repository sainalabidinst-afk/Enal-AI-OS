from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    agent: str | None = None


class AgentConfig(BaseModel):
    name: str
    role: str
    description: str
    tools: list[str] = []
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096


class Task(BaseModel):
    id: str
    description: str
    agent: str
    status: str = "pending"
    result: str | None = None
    error: str | None = None


class Plan(BaseModel):
    id: str
    user_request: str
    tasks: list[Task]
    status: str = "planning"
    final_result: str | None = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    workspace_id: str | None = None
    stream: bool = False


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    agent: str
    tasks_completed: int = 0
    metadata: dict[str, Any] = {}
    analysis: dict[str, Any] | None = None
