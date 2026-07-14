import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class SpanType(str, Enum):
    AGENT = "agent"
    TOOL = "tool"
    LLM = "llm"
    WORKFLOW = "workflow"
    TASK = "task"


@dataclass
class TraceSpan:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    parent_id: str | None = None
    span_type: SpanType = SpanType.AGENT
    name: str = ""
    agent: str = ""
    input: Any = None
    output: Any = None
    tokens_used: int = 0
    cost: float = 0.0
    latency_ms: float = 0.0
    success: bool = True
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None


class Observability:
    def __init__(self):
        self._traces: dict[str, list[TraceSpan]] = {}
        self._current_trace: str | None = None

    def start_trace(self, name: str) -> str:
        trace_id = str(uuid.uuid4())
        self._traces[trace_id] = []
        self._current_trace = trace_id
        span = TraceSpan(trace_id=trace_id, span_type=SpanType.WORKFLOW, name=name)
        self._traces[trace_id].append(span)
        return trace_id

    def start_span(self, name: str, span_type: SpanType = SpanType.AGENT, agent: str = "", parent_id: str | None = None) -> TraceSpan:
        trace_id = self._current_trace or str(uuid.uuid4())
        if trace_id not in self._traces:
            self._traces[trace_id] = []
        span = TraceSpan(
            trace_id=trace_id,
            parent_id=parent_id,
            span_type=span_type,
            name=name,
            agent=agent,
            started_at=datetime.utcnow(),
        )
        self._traces[trace_id].append(span)
        return span

    def end_span(self, span: TraceSpan, output: Any = None, error: str | None = None):
        span.finished_at = datetime.utcnow()
        span.latency_ms = (span.finished_at - span.started_at).total_seconds() * 1000
        span.output = output
        span.error = error
        span.success = error is None

    def get_trace(self, trace_id: str) -> list[dict[str, Any]]:
        spans = self._traces.get(trace_id, [])
        return [
            {
                "id": s.id,
                "trace_id": s.trace_id,
                "parent_id": s.parent_id,
                "type": s.span_type.value,
                "name": s.name,
                "agent": s.agent,
                "latency_ms": s.latency_ms,
                "tokens": s.tokens_used,
                "cost": s.cost,
                "success": s.success,
                "error": s.error,
            }
            for s in spans
        ]

    def get_metrics(self, agent: str | None = None) -> dict[str, Any]:
        all_spans = [s for spans in self._traces.values() for s in spans]
        if agent:
            all_spans = [s for s in all_spans if s.agent == agent]
        return {
            "total_spans": len(all_spans),
            "success_rate": sum(1 for s in all_spans if s.success) / len(all_spans) if all_spans else 0,
            "avg_latency_ms": sum(s.latency_ms for s in all_spans) / len(all_spans) if all_spans else 0,
            "total_cost": sum(s.cost for s in all_spans),
            "total_tokens": sum(s.tokens_used for s in all_spans),
        }


observability = Observability()
