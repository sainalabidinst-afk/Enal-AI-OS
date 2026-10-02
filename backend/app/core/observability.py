import logging  # noqa: I001
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum, Enum  # noqa: F401
from typing import Any

logger = logging.getLogger(__name__)


class SpanType(StrEnum):
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
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None


class AnomalyType(StrEnum):
    """Types of anomalies that can be detected."""

    SPAM = "spam"
    TOXICITY = "toxicity"
    HALLUCINATION = "hallucination"
    BIAS = "bias"
    COST_SPIKE = "cost_spike"
    LATENCY_SPIKE = "latency_spike"
    FREQUENCY_SPIKE = "frequency_spike"


@dataclass
class AnomalyResult:
    """Result of an anomaly detection check."""

    detected: bool
    anomaly_type: str = ""
    score: float = 0.0
    threshold: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""


class Observability:
    def __init__(self):
        self._traces: dict[str, list[TraceSpan]] = {}
        self._current_trace: str | None = None
        self._context: dict[str, str] = {}

    def start_trace(self, name: str) -> str:
        trace_id = str(uuid.uuid4())
        self._traces[trace_id] = []
        self._current_trace = trace_id
        span = TraceSpan(trace_id=trace_id, span_type=SpanType.WORKFLOW, name=name)
        self._traces[trace_id].append(span)
        return trace_id

    def start_span(self, name: str, span_type: SpanType = SpanType.AGENT, agent: str = "", parent_id: str | None = None) -> TraceSpan:  # noqa: E501
        trace_id = self._current_trace or str(uuid.uuid4())
        if trace_id not in self._traces:
            self._traces[trace_id] = []
        span = TraceSpan(
            trace_id=trace_id,
            parent_id=parent_id,
            span_type=span_type,
            name=name,
            agent=agent,
            started_at=datetime.now(UTC),
        )
        self._traces[trace_id].append(span)
        return span

    def end_span(self, span: TraceSpan, output: Any = None, error: str | None = None):
        span.finished_at = datetime.now(UTC)
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
            "success_rate": sum(1 for s in all_spans if s.success) / len(all_spans) if all_spans else 0,  # noqa: E501
            "avg_latency_ms": sum(s.latency_ms for s in all_spans) / len(all_spans) if all_spans else 0,  # noqa: E501
            "total_cost": sum(s.cost for s in all_spans),
            "total_tokens": sum(s.tokens_used for s in all_spans),
        }
    def inject_context(self, trace_id: str, parent_id: str | None = None) -> dict[str, str]:
        return {"trace_id": trace_id, "parent_id": parent_id or ""}

    def extract_context(self, headers: dict[str, str]) -> tuple[str, str | None]:
        return headers.get("trace_id", ""), headers.get("parent_id") or None

    def propagate_context(self, trace_id: str) -> str:
        return f"trace_id={trace_id}"

    def anomaly_detect(
        self,
        metric_name: str,
        value: float,
        baseline: float | None = None,
        history: list[float] | None = None,
    ) -> AnomalyResult:
        """Detect anomalies in metrics using Z-score and threshold methods.

        Uses baseline deviation: if value deviates > 2 standard deviations from
        baseline/history, flag as anomaly.
        """
        history = history or []

        if baseline is not None:
            if value > baseline * 1.5:
                anomaly_type = (
                    AnomalyType.COST_SPIKE
                    if "cost" in metric_name
                    else AnomalyType.LATENCY_SPIKE
                )
                return AnomalyResult(
                    detected=True,
                    anomaly_type=anomaly_type,
                    score=value / baseline if baseline else 0,
                    threshold=baseline * 1.5,
                    details={
                        "metric": metric_name,
                        "value": value,
                        "baseline": baseline,
                    },
                    recommendation=(
                        f"Investigate {metric_name}: {value} "
                        f"exceeds baseline {baseline} by 50%"
                    ),
                )

        if len(history) >= 3:
            mean_val = sum(history) / len(history)
            variance = sum((x - mean_val) ** 2 for x in history) / len(history)
            std_dev = variance ** 0.5

            if std_dev > 0:
                z_score = abs(value - mean_val) / std_dev
                if z_score > 2.0:
                    return AnomalyResult(
                        detected=True,
                        anomaly_type=AnomalyType.FREQUENCY_SPIKE,
                        score=z_score,
                        threshold=2.0,
                        details={
                            "metric": metric_name,
                            "value": value,
                            "mean": mean_val,
                            "std_dev": std_dev,
                        },
                        recommendation=f"Anomaly detected in {metric_name}: Z-score={z_score:.2f}",
                    )

        return AnomalyResult(
            detected=False,
            anomaly_type="",
            score=0.0,
            details={"metric": metric_name, "value": value},
        )

    def check_span_anomaly(self, span: TraceSpan) -> AnomalyResult:
        """Check if a trace span has anomalous characteristics."""
        issues = []

        if span.error and span.success is False:
            issues.append(f"span error: {span.error}")
        if span.latency_ms > 5000:
            issues.append(f"high latency: {span.latency_ms}ms")
        if span.tokens_used > 8000:
            issues.append(f"high token count: {span.tokens_used}")

        if issues:
            anomaly_type = (
                AnomalyType.HALLUCINATION
                if "error" in str(issues)
                else AnomalyType.LATENCY_SPIKE
            )
            return AnomalyResult(
                detected=True,
                anomaly_type=anomaly_type,
                score=1.0 if len(issues) > 1 else 0.7,
                details={
                    "span_name": span.name,
                    "issues": issues,
                },
                recommendation=f"Review span '{span.name}': {'; '.join(issues)}",
            )

        return AnomalyResult(detected=False)



observability = Observability()

