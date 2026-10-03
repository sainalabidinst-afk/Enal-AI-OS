"""
Observability log for Translator Expert.

Provides structured logging for translation operations with metrics
for latency, accuracy, and throughput — integrated with the core
Observability tracing system.
"""

import logging
from typing import Any

from backend.app.runtime import SpanType, observability

logger = logging.getLogger(__name__)

CAPABILITY_ID = "translator-expert"


def start_translation_trace(
    text: str,
    source_lang: str,
    target_lang: str,
    domain: str,
    style: str,
) -> tuple[str, Any]:
    """Begin an observability trace for a translation operation.

    Returns (trace_id, span) so the caller can end the span later.
    """
    trace_id = observability.start_trace(f"translation:{source_lang}→{target_lang}")
    span = observability.start_span(
        name=f"translate:{domain}:{style}",
        span_type=SpanType.AGENT,
        agent=CAPABILITY_ID,
        parent_id=None,
    )
    span.metadata = {
        "language_pair": f"{source_lang}→{target_lang}",
        "domain": domain,
        "style": style,
        "text_length": len(text),
    }
    logger.info(
        "Translation started: trace=%s pair=%s→%s domain=%s style=%s",
        trace_id,
        source_lang,
        target_lang,
        domain,
        style,
    )
    return trace_id, span


def log_translation_complete(
    span: Any,
    result: dict[str, Any],
    duration_ms: float,
) -> None:
    """Record a successful translation span with metrics."""
    span.latency_ms = duration_ms
    span.tokens_used = result.get("token_count", 0)
    span.output = result
    span.success = True
    observability.end_span(span, output=result)
    record_translation_metric(
        source_lang=result.get("source_language", "unknown"),
        target_lang=result.get("target_language", "unknown"),
        domain=result.get("domain", "general"),
        latency_ms=duration_ms,
        accuracy=result.get("quality_score", 0.0),
        confidence=result.get("confidence", 0.0),
    )
    logger.info(
        "Translation complete: span=%s duration=%.2fms confidence=%.2f",
        span.id,
        duration_ms,
        result.get("confidence", 0.0),
    )


def log_translation_error(
    span: Any,
    error: Exception,
    duration_ms: float,
) -> None:
    """Record a failed translation span."""
    span.latency_ms = duration_ms
    span.error = str(error)
    span.success = False
    observability.end_span(span, error=str(error))
    logger.error(
        "Translation failed: span=%s error=%s duration=%.2fms",
        span.id,
        error,
        duration_ms,
    )


def record_translation_metric(
    source_lang: str,
    target_lang: str,
    domain: str,
    latency_ms: float,
    accuracy: float,
    confidence: float,
    throughput_chars_per_sec: float | None = None,
) -> dict[str, Any]:
    """Record a single translation metric sample to the in-memory log."""
    from apps.translator_expert.observability_metrics import (
        TranslationMetricsCollector,
    )

    collector = TranslationMetricsCollector.get_instance()
    return collector.record(
        source_lang=source_lang,
        target_lang=target_lang,
        domain=domain,
        latency_ms=latency_ms,
        accuracy=accuracy,
        confidence=confidence,
        throughput_chars_per_sec=throughput_chars_per_sec,
    )


def get_translation_metrics(
    source_lang: str | None = None,
    target_lang: str | None = None,
    domain: str | None = None,
    limit: int = 1000,
) -> list[dict[str, Any]]:
    """Retrieve recorded translation metrics, optionally filtered."""
    from apps.translator_expert.observability_metrics import (
        TranslationMetricsCollector,
    )

    collector = TranslationMetricsCollector.get_instance()
    return collector.get_metrics(
        source_lang=source_lang,
        target_lang=target_lang,
        domain=domain,
        limit=limit,
    )


def get_translation_summary() -> dict[str, Any]:
    """Return aggregated summary of translation metrics."""
    from apps.translator_expert.observability_metrics import (
        TranslationMetricsCollector,
    )

    collector = TranslationMetricsCollector.get_instance()
    return collector.get_summary()


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
    "log_translation_complete",
    "log_translation_error",
    "record_translation_metric",
    "get_translation_metrics",
    "get_translation_summary",
    "start_translation_trace",
    "CAPABILITY_ID",
]
