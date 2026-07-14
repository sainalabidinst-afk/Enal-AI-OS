from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent: Optional[str] = None


class AgentConfig(BaseModel):
    name: str
    role: str
    description: str
    tools: List[str] = []
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096


class Task(BaseModel):
    id: str
    description: str
    agent: str
    status: str = "pending"
    result: Optional[str] = None
    error: Optional[str] = None


class Plan(BaseModel):
    id: str
    user_request: str
    tasks: List[Task]
    status: str = "planning"
    final_result: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    workspace_id: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    agent: str
    tasks_completed: int = 0
    metadata: Dict[str, Any] = {}
    analysis: Optional[Dict[str, Any]] = None
