"""
Tests for Observability & Distributed Tracing
============================================
Tests for trace propagation and context management.
"""



class TestObservabilityDistributedTracing:
    """Tests for distributed tracing features."""

    def test_inject_context(self):
        from backend.app.core.observability import Observability
        obs = Observability()
        ctx = obs.inject_context("trace-123", "parent-456")
        assert ctx["trace_id"] == "trace-123"
        assert ctx["parent_id"] == "parent-456"

    def test_extract_context(self):
        from backend.app.core.observability import Observability
        obs = Observability()
        headers = {"trace_id": "trace-abc", "parent_id": "parent-xyz"}
        trace_id, parent_id = obs.extract_context(headers)
        assert trace_id == "trace-abc"
        assert parent_id == "parent-xyz"

    def test_propagate_context(self):
        from backend.app.core.observability import Observability
        obs = Observability()
        propagated = obs.propagate_context("trace-789")
        assert "trace-789" in propagated

    def test_trace_context_flow(self):
        from backend.app.core.observability import Observability, SpanType
        obs = Observability()
        trace_id = obs.start_trace("test-workflow")
        ctx = obs.inject_context(trace_id, None)
        obs._current_trace = trace_id
        span = obs.start_span("test-task", SpanType.TASK)
        obs.end_span(span, output={"status": "ok"})
        assert span.trace_id == trace_id
        assert span.success is True


class TestObservabilityMetrics:
    """Tests for observability metrics."""

    def test_metrics_empty(self):
        from backend.app.core.observability import Observability
        obs = Observability()
        metrics = obs.get_metrics()
        assert metrics["total_spans"] == 0

    def test_metrics_with_spans(self):
        from backend.app.core.observability import Observability, SpanType
        obs = Observability()
        trace_id = obs.start_trace("test")
        span = obs.start_span("task1", SpanType.TASK)
        obs.end_span(span, output="ok")
        metrics = obs.get_metrics()
        assert metrics["total_spans"] == 2


class TestTraceSpan:
    """Tests for TraceSpan."""

    def test_span_creation(self):
        from backend.app.core.observability import SpanType, TraceSpan
        span = TraceSpan(
            trace_id="trace-1",
            span_type=SpanType.LLM,
            name="test-span",
            agent="test-agent",
        )
        assert span.name == "test-span"
        assert span.span_type == SpanType.LLM
        assert span.success is True