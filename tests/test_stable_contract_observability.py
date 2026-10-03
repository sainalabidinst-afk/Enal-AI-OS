"""
Tests for RFC-0001 Observability Layer — enhanced with structured logging
and metrics, plus existing tracing functionality.
"""

import json
import logging

import pytest

from backend.app.core.observability import (
    MetricsCollector,
    Observability,
    SpanType,
    StructuredLogger,
    metrics_collector,
    structured_logger,
)


class TestStructuredLogger:
    def test_log_with_fields(self, caplog):
        logger = StructuredLogger("test_logger")
        with caplog.at_level(logging.INFO):
            logger.info("test message", task_id="t1", pack="code_engineer")

        assert "test message" in caplog.text
        log_data = json.loads(caplog.records[0].getMessage())
        assert log_data["message"] == "test message"
        assert log_data["task_id"] == "t1"
        assert log_data["pack"] == "code_engineer"

    def test_sensitive_data_redacted(self, caplog):
        logger = StructuredLogger("test_security")
        with caplog.at_level(logging.INFO):
            logger.info("login attempt", password="secret123", token="abc")

        log_data = json.loads(caplog.records[0].getMessage())
        assert log_data["password"] == "***REDACTED***"
        assert log_data["token"] == "***REDACTED***"

    def test_debug_level(self, caplog):
        logger = StructuredLogger("test_debug")
        with caplog.at_level(logging.DEBUG):
            logger.debug("debug msg", detail="info")
        assert "debug msg" in caplog.text

    def test_error_level(self, caplog):
        logger = StructuredLogger("test_error")
        with caplog.at_level(logging.ERROR):
            logger.error("error msg", error_code=500)
        assert "error msg" in caplog.text


class TestMetricsCollector:
    @pytest.fixture
    def mc(self):
        mc = MetricsCollector()
        yield mc
        mc.reset()

    def test_increment_counter(self, mc):
        mc.increment("requests", 1)
        mc.increment("requests", 1)
        metrics = mc.get_metrics()
        assert metrics["counters"]["requests"] == 2

    def test_gauge(self, mc):
        mc.gauge("memory_mb", 128.5)
        metrics = mc.get_metrics()
        assert metrics["gauges"]["memory_mb"] == 128.5

    def test_histogram(self, mc):
        for val in [10, 20, 30, 40, 50]:
            mc.histogram("latency_ms", val)
        metrics = mc.get_metrics()
        h = metrics["histograms"]["latency_ms"]
        assert h["count"] == 5
        assert h["min"] == 10
        assert h["max"] == 50
        assert h["avg"] == 30.0
        assert h["p50"] == 30
        assert h["p95"] == 50

    def test_increment_with_tags(self, mc):
        mc.increment("requests", 1, tags={"pack": "code_engineer"})
        mc.increment("requests", 1, tags={"pack": "network_engineer"})
        metrics = mc.get_metrics()
        assert "requests|pack=code_engineer" in metrics["counters"]
        assert "requests|pack=network_engineer" in metrics["counters"]

    def test_reset(self, mc):
        mc.increment("test", 1)
        mc.reset()
        metrics = mc.get_metrics()
        assert metrics["counters"] == {}

    def test_empty_histogram(self, mc):
        mc.histogram("empty", 0)
        metrics = mc.get_metrics()
        # After recording 0, histogram should have 1 entry
        h = metrics["histograms"]["empty"]
        assert h["count"] == 1


class TestObservabilityTracing:
    @pytest.fixture
    def obs(self):
        return Observability()

    def test_start_trace(self, obs):
        trace_id = obs.start_trace("test_trace")
        assert len(trace_id) > 0
        assert obs._current_trace == trace_id

    def test_start_span_within_trace(self, obs):
        trace_id = obs.start_trace("test")
        span = obs.start_span("step1", SpanType.TASK)
        assert span.trace_id == trace_id
        obs.end_span(span, output={"result": "ok"})
        assert span.latency_ms >= 0

    def test_end_span_with_error(self, obs):
        obs.start_trace("test")
        span = obs.start_span("step1", SpanType.TASK)
        obs.end_span(span, error="something failed")
        assert span.success is False
        assert span.error == "something failed"

    def test_get_trace(self, obs):
        trace_id = obs.start_trace("test")
        span = obs.start_span("task", SpanType.TASK)
        obs.end_span(span)
        trace = obs.get_trace(trace_id)
        assert len(trace) == 2
        assert trace[1]["name"] == "task"

    def test_get_metrics(self, obs):
        obs.start_trace("test")
        span = obs.start_span("task", SpanType.AGENT, agent="test_agent")
        obs.end_span(span)
        metrics = obs.get_metrics(agent="test_agent")
        assert metrics["total_spans"] == 1

    def test_context_propagation(self, obs):
        trace_id = obs.start_trace("test")
        ctx = obs.inject_context(trace_id, parent_id="parent-1")
        assert ctx["trace_id"] == trace_id
        assert ctx["parent_id"] == "parent-1"

    def test_extract_context(self, obs):
        headers = {"trace_id": "abc", "parent_id": "def"}
        trace_id, parent_id = obs.extract_context(headers)
        assert trace_id == "abc"
        assert parent_id == "def"


class TestModuleSingletons:
    def test_structured_logger_instance(self):
        assert isinstance(structured_logger, StructuredLogger)

    def test_metrics_collector_instance(self):
        assert isinstance(metrics_collector, MetricsCollector)
