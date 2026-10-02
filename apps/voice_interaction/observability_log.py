"""
Observability logging for Voice Interaction.

Integrates with the core Observability system via the runtime facade to
provide structured tracing for voice operations (transcription, synthesis).
"""

import logging
from typing import Any

from backend.app.runtime import SpanType, observability

logger = logging.getLogger(__name__)

CAPABILITY_ID = "voice-interaction"


def start_voice_trace(
    operation: str,
    language: str,
    provider: str,
) -> tuple[str, Any]:
    """Begin an observability trace for a voice operation.

    Returns (trace_id, span) so the caller can end the span later.
    """
    trace_id = observability.start_trace(f"voice:{operation}:{language}")
    span = observability.start_span(
        name=f"voice:{operation}:{provider}",
        span_type=SpanType.AGENT,
        agent=CAPABILITY_ID,
        parent_id=None,
    )
    span.metadata = {
        "operation": operation,
        "language": language,
        "provider": provider,
    }
    logger.info(
        "Voice operation started: trace=%s op=%s lang=%s provider=%s",
        trace_id,
        operation,
        language,
        provider,
    )
    return trace_id, span


def log_voice_complete(
    span: Any,
    result: dict[str, Any],
    duration_ms: float,
) -> None:
    """Record a successful voice operation span with metrics."""
    span.latency_ms = duration_ms
    span.output = result
    span.success = True
    observability.end_span(span, output=result)
    logger.info(
        "Voice operation complete: span=%s duration=%.2fms",
        span.id,
        duration_ms,
    )


def log_voice_error(
    span: Any,
    error: Exception,
    duration_ms: float,
) -> None:
    """Record a failed voice operation span."""
    span.latency_ms = duration_ms
    span.error = str(error)
    span.success = False
    observability.end_span(span, error=str(error))
    logger.error(
        "Voice operation failed: span=%s error=%s duration=%.2fms",
        span.id,
        error,
        duration_ms,
    )


def log_execution(capability_id: str, operation: str, duration_ms: float) -> None:
    """Log capability execution (compatibility with pack convention)."""
    logger.info(
        "Capability %s executed %s in %.2fms",
        capability_id,
        operation,
        duration_ms,
    )


def log_error(capability_id: str, operation: str, error: Exception) -> None:
    """Log capability error (compatibility with pack convention)."""
    logger.error("Capability %s failed %s: %s", capability_id, operation, error)


__all__ = [
    "log_execution",
    "log_error",
    "log_voice_complete",
    "log_voice_error",
    "start_voice_trace",
    "CAPABILITY_ID",
]
