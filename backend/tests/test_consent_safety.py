"""Tests for consent & safety (Phase 3)."""

import asyncio
from datetime import timedelta

from backend.app.core.consent import (
    ConsentManager,
    ConsentRequest,
    ConsentStatus,
    RiskLevel,
    classify_risk,
    consent_manager,
)
from backend.app.core.observability import (
    AnomalyType,
    SpanType,
    TraceSpan,
    observability,
)


def _run(coro):
    """Run an async coroutine synchronously for testing."""
    return asyncio.new_event_loop().run_until_complete(coro)


class TestRiskClassification:
    """Tests for classify_risk."""

    def test_low_risk_actions(self):
        """Read-only actions are classified as low risk."""
        assert classify_risk("read_file") == RiskLevel.LOW
        assert classify_risk("list_directory") == RiskLevel.LOW
        assert classify_risk("list_events") == RiskLevel.LOW

    def test_medium_risk_actions(self):
        """Write/email/send actions are classified as medium risk."""
        assert classify_risk("write_file") == RiskLevel.MEDIUM
        assert classify_risk("send_email") == RiskLevel.MEDIUM
        assert classify_risk("create_event") == RiskLevel.MEDIUM

    def test_high_risk_actions(self):
        """Trading and system actions are high risk."""
        assert classify_risk("trading") == RiskLevel.HIGH
        assert classify_risk("system_config") == RiskLevel.HIGH
        assert classify_risk("system_restart") == RiskLevel.HIGH

    def test_unknown_action_defaults_medium(self):
        """Unknown actions default to medium risk."""
        result = classify_risk("unknown_action", {"connector_type": ""})
        assert result == RiskLevel.MEDIUM


class TestConsentManager:
    """Tests for ConsentManager."""

    def test_request_created_pending(self):
        """Consent request starts in PENDING state."""
        mgr = ConsentManager(default_timeout=30)
        r = mgr.request(
            action_type="send_email",
            description="Send email to team",
        )
        assert r.status == ConsentStatus.PENDING
        assert r.risk_level == RiskLevel.MEDIUM
        assert r.is_resolved is False

    def test_approve(self):
        """Approval sets status to APPROVED."""
        mgr = ConsentManager()
        r = mgr.request(action_type="read_file", description="Read file")
        result = mgr.approve(r.request_id)
        assert result.status == ConsentStatus.APPROVED
        assert result.responder == "user"
        assert result.response_at is not None

    def test_deny(self):
        """Deny sets status to DENIED."""
        mgr = ConsentManager()
        r = mgr.request(action_type="delete_file", description="Delete file")
        result = mgr.deny(r.request_id)
        assert result.status == ConsentStatus.DENIED

    def test_get_pending_count(self):
        """Pending count tracks unexpired requests."""
        mgr = ConsentManager(default_timeout=30)
        mgr.request(action_type="read_file", description="test")
        mgr.request(action_type="read_file", description="test")
        assert mgr.get_pending_count() == 2
        mgr.approve(mgr._history[0].request_id)
        assert mgr.get_pending_count() == 1

    def test_timeout_expired(self):
        """Expired requests are marked EXPIRED."""
        mgr = ConsentManager(default_timeout=0)
        r = mgr.request(action_type="read_file", description="test")
        status = mgr.check_timeout(r.request_id)
        assert status == ConsentStatus.EXPIRED
        assert r.is_resolved

    def test_approve_already_resolved(self):
        """Cannot approve an already-resolved request."""
        mgr = ConsentManager()
        r = mgr.request(action_type="read_file", description="test")
        mgr.approve(r.request_id)
        result = mgr.approve(r.request_id)
        assert result.status == ConsentStatus.APPROVED

    def test_unknown_request(self):
        """Approving unknown request returns None."""
        mgr = ConsentManager()
        result = mgr.approve("unknown-id")
        assert result is None

    def test_cleanup(self):
        """Cleanup expires stale pending requests."""
        mgr = ConsentManager(default_timeout=0)
        r = mgr.request(action_type="read_file", description="test")
        removed = mgr.cleanup()
        assert removed == 1
        assert r.status == ConsentStatus.EXPIRED


class TestConsentRequest:
    """Tests for ConsentRequest dataclass."""

    def test_defaults(self):
        """ConsentRequest has proper defaults."""
        r = ConsentRequest(
            action_type="test",
            description="test action",
        )
        assert r.status == ConsentStatus.PENDING
        assert r.risk_level == RiskLevel.LOW
        assert r.timeout_seconds == 30
        assert r.is_expired is False

    def test_expiry_property(self):
        """expires_at is created_at + timeout_seconds."""
        r = ConsentRequest(
            action_type="test",
            description="test",
            timeout_seconds=60,
        )
        expected = r.created_at + timedelta(seconds=60)
        assert r.expires_at == expected


class TestAnomalyDetection:
    """Tests for observability.anomaly_detect."""

    def test_normal_value_no_anomaly(self):
        """Normal values don't trigger anomaly."""
        result = observability.anomaly_detect(
            metric_name="latency_ms",
            value=200,
            baseline=190,
            history=[198, 195, 202, 200],
        )
        assert not result.detected

    def test_cost_spike_anomaly(self):
        """Value exceeding 1.5x baseline is flagged."""
        result = observability.anomaly_detect(
            metric_name="total_cost",
            value=300,
            baseline=100,
        )
        assert result.detected
        assert result.anomaly_type == AnomalyType.COST_SPIKE

    def test_latency_spike_anomaly(self):
        """Latency spike detected via baseline."""
        result = observability.anomaly_detect(
            metric_name="avg_latency_ms",
            value=1000,
            baseline=100,
        )
        assert result.detected
        assert result.anomaly_type == AnomalyType.LATENCY_SPIKE

    def test_zscore_anomaly(self):
        """Z-score > 2.0 from history triggers anomaly."""
        result = observability.anomaly_detect(
            metric_name="error_rate",
            value=50,
            history=[1, 2, 1, 0, 2, 1, 1, 0, 1],
        )
        assert result.detected
        assert result.anomaly_type == AnomalyType.FREQUENCY_SPIKE

    def test_no_baseline_no_history(self):
        """Without baseline or history, no anomaly."""
        result = observability.anomaly_detect(
            metric_name="test",
            value=42,
        )
        assert not result.detected
        assert result.score == 0.0


class TestSpanAnomaly:
    """Tests for check_span_anomaly."""

    def test_clean_span_no_anomaly(self):
        """A clean span with no errors has no anomaly."""
        span = TraceSpan(
            name="test_span",
            span_type=SpanType.AGENT,
            agent="jenny",
            latency_ms=100,
            tokens_used=50,
            success=True,
        )
        result = observability.check_span_anomaly(span)
        assert not result.detected

    def test_error_span_anomaly(self):
        """A span with error triggers anomaly."""
        span = TraceSpan(
            name="test_span",
            span_type=SpanType.AGENT,
            agent="jenny",
            success=False,
            error="timeout",
            latency_ms=100,
            tokens_used=50,
        )
        result = observability.check_span_anomaly(span)
        assert result.detected
        assert result.anomaly_type == AnomalyType.HALLUCINATION

    def test_high_latency_anomaly(self):
        """A span with latency > 5s triggers anomaly."""
        span = TraceSpan(
            name="slow_span",
            span_type=SpanType.AGENT,
            agent="jenny",
            latency_ms=6000,
            tokens_used=50,
            success=True,
        )
        result = observability.check_span_anomaly(span)
        assert result.detected


class TestConsentAPI:
    """Tests for consent API endpoints via the API test client pattern."""

    def test_consent_manager_singleton(self):
        """consent_manager is a singleton instance."""
        assert consent_manager is not None
        assert hasattr(consent_manager, "request")
        assert hasattr(consent_manager, "approve")
        assert hasattr(consent_manager, "deny")
