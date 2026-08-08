from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(str, Enum):
    analysis = "analysis"
    chat = "chat"
    parser = "parser"
    reasoning = "reasoning"


class Status(str, Enum):
    success = "success"
    error = "error"


@dataclass
class AnalysisEvent:
    event_type: str = "analysis"
    analysis_id: str = ""
    timestamp: str = ""
    status: str = Status.success
    error: str | None = None
    workspace_id: str = ""
    vendor: str = ""
    device_type: str = ""
    files: int = 0
    size_bytes: int = 0
    parser: str = ""
    analysis_time_ms: float = 0.0
    reasoning_time_ms: float = 0.0
    report_time_ms: float = 0.0
    total_time_ms: float = 0.0
    findings: int = 0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    confidence: float = 0.0
    compliance_score: float | None = None
    executive_report: bool = False
    accepted: bool = False
    false_positive: int = 0
    false_negative: int = 0
    engineer_rating: int = 0
    report_used: bool = False
    benchmark_case_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatEvent:
    event_type: str = "chat"
    chat_id: str = ""
    timestamp: str = ""
    status: str = Status.success
    error: str | None = None
    workspace_id: str = ""
    conversation_id: str = ""
    message_length: int = 0
    response_length: int = 0
    total_time_ms: float = 0.0
    tasks_completed: int = 0
    has_execution: bool = False
    agent: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParserEvent:
    event_type: str = "parser"
    parser_name: str = ""
    timestamp: str = ""
    status: str = Status.success
    error: str | None = None
    vendor: str = ""
    device_role: str = ""
    attachment_type: str = ""
    parse_time_ms: float = 0.0
    findings: int = 0
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningEvent:
    event_type: str = "reasoning"
    reasoning_id: str = ""
    timestamp: str = ""
    status: str = Status.success
    error: str | None = None
    vendor: str = ""
    device_type: str = ""
    reasoning_time_ms: float = 0.0
    findings: int = 0
    confidence: float = 0.0
    compliance_score: float | None = None
    recommendations: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
