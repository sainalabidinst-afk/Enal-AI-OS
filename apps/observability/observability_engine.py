"""
Observability Capability Pack — Observability Analysis Engine module.
"""

from __future__ import annotations

import logging
import statistics
from typing import Any

from apps.observability.schemas import (
    AnomalyFinding,
    AnomalyReport,
    LogEntry,
    LogPattern,
    MetricSample,
    MetricSummary,
    ObservabilityInputs,
    ObservabilityOperation,
    TraceSpan,
    TraceSummary,
)

logger = logging.getLogger(__name__)


class ObservabilityAnalysisEngine:
    """
    Provides metrics collection, distributed trace analysis, log analysis,
    and anomaly detection.

    All calculations use explicit inputs and declared formulae; no silent
    defaults are applied for missing values.
    """

    ERROR_BUDGET_THRESHOLD: float = 0.05

    def check_input_validation(self, inputs: ObservabilityInputs) -> dict[str, Any]:
        """Validate inputs for missing or ambiguous values."""
        errors: list[str] = []
        valid = True

        if inputs.operation == ObservabilityOperation.metrics_collect:
            if inputs.metric_name is None:
                errors.append("metric_name is required for metrics_collect")
                valid = False
        if inputs.operation == ObservabilityOperation.trace_analyze:
            if inputs.service_name is None and inputs.trace_id is None:
                errors.append("service_name or trace_id is required for trace_analyze")
                valid = False
        if inputs.operation == ObservabilityOperation.log_analyze:
            if not inputs.log_entries and not inputs.pattern:
                errors.append("log_entries or pattern is required for log_analyze")
                valid = False
        if inputs.operation == ObservabilityOperation.anomaly_detect:
            if inputs.metric_name is None:
                errors.append("metric_name is required for anomaly_detect")
                valid = False
            if inputs.baseline is None and not inputs.data_points:
                errors.append("baseline or data_points is required for anomaly_detect")
                valid = False

        return {
            "valid": valid and len(errors) == 0,
            "validation_errors": errors,
            "calculation_performed": valid,
        }

    def _collect_values(self, inputs: ObservabilityInputs) -> list[float]:
        """Gather numeric values from explicit samples and historical values."""
        values: list[float] = []
        values.extend(inputs.historical_values)
        for sample in inputs.metric_samples:
            values.append(sample.value)
        if inputs.current_value is not None:
            values.append(inputs.current_value)
        return [v for v in values if v is not None]

    def collect_metrics(self, inputs: ObservabilityInputs) -> MetricSummary:
        """Summarize observed metrics and evaluate threshold breaches."""
        values = self._collect_values(inputs)
        current = inputs.current_value

        if values:
            average = round(statistics.fmean(values), 4)
            maximum = round(max(values), 4)
            minimum = round(min(values), 4)
        else:
            average = None
            maximum = None
            minimum = None

        breached = self._is_threshold_breached(current, inputs.threshold, inputs.threshold_direction)

        unit = inputs.metric_samples[0].unit if inputs.metric_samples else ""
        inputs_traced = ["metric_name", "current_value", "historical_values"]

        return MetricSummary(
            metric_name=inputs.metric_name or "unknown",
            current_value=current,
            average=average,
            maximum=maximum,
            minimum=minimum,
            threshold=inputs.threshold,
            threshold_direction=inputs.threshold_direction,
            breached=breached,
            unit=unit,
            formula="avg/max/min from collected values; breached = current vs threshold",
            inputs_traced=inputs_traced,
        )

    def _is_threshold_breached(
        self,
        current: float | None,
        threshold: float | None,
        direction: str | None,
    ) -> bool:
        if current is None or threshold is None or direction is None:
            return False
        if direction == "above":
            return current > threshold
        if direction == "below":
            return current < threshold
        return False

    def analyze_trace(self, inputs: ObservabilityInputs) -> TraceSummary:
        """Summarize a distributed trace and its health."""
        spans: list[TraceSpan] = list(inputs.spans)
        if inputs.duration_ms is not None:
            total_duration = inputs.duration_ms
        else:
            total_duration = round(sum(s.duration_ms for s in spans), 4) if spans else None

        span_count = inputs.span_count if inputs.span_count is not None else len(spans)
        error_rate = inputs.error_rate

        if inputs.p95_latency_ms is not None:
            p95 = inputs.p95_latency_ms
        elif spans:
            durations = sorted(s.duration_ms for s in spans)
            p95 = round(durations[int(len(durations) * 0.95) - 1], 4) if len(durations) > 0 else None
        else:
            p95 = None

        healthy = True
        if error_rate is not None:
            healthy = error_rate <= self.ERROR_BUDGET_THRESHOLD

        return TraceSummary(
            service_name=inputs.service_name or "unknown",
            trace_id=inputs.trace_id,
            total_duration_ms=total_duration,
            span_count=span_count,
            error_rate=error_rate,
            healthy=healthy,
            p95_latency_ms=p95,
        )

    def analyze_log(self, inputs: ObservabilityInputs) -> list[LogPattern]:
        """Group log entries into patterns by level and matched pattern."""
        entries: list[LogEntry] = list(inputs.log_entries)
        patterns: list[LogPattern] = []

        if not entries:
            if inputs.pattern:
                patterns.append(LogPattern(
                    pattern=inputs.pattern,
                    level=inputs.log_level,
                    count=0,
                    services=[],
                    severity="",
                ))
            return patterns

        # Group by log level when no explicit pattern is supplied.
        if inputs.pattern:
            matched = [e for e in entries if inputs.pattern.lower() in e.message.lower()]
            services = sorted({e.service for e in matched if e.service})
            levels = sorted({e.level for e in matched if e.level})
            patterns.append(LogPattern(
                pattern=inputs.pattern,
                level=",".join(levels) if levels else inputs.log_level,
                count=len(matched),
                services=services,
                severity=self._severity_for_level(levels[0]) if levels else "",
            ))
        else:
            seen: dict[str, list[LogEntry]] = {}
            for entry in entries:
                seen.setdefault(entry.level or "unknown", []).append(entry)
            for level, group in seen.items():
                services = sorted({e.service for e in group if e.service})
                patterns.append(LogPattern(
                    pattern=f"level:{level}",
                    level=level,
                    count=len(group),
                    services=services,
                    severity=self._severity_for_level(level),
                ))

        return patterns

    @staticmethod
    def _severity_for_level(level: str) -> str:
        mapping = {
            "critical": "critical",
            "error": "high",
            "warning": "medium",
            "info": "low",
            "debug": "info",
        }
        return mapping.get(level.lower(), "")

    def detect_anomaly(self, inputs: ObservabilityInputs) -> AnomalyReport:
        """Detect anomalies by comparing observed values to a baseline."""
        values = self._collect_values(inputs)
        current = inputs.current_value if inputs.current_value is not None else (
            values[-1] if values else None
        )

        baseline = inputs.baseline
        threshold = inputs.threshold
        direction = inputs.threshold_direction

        deviation_pct: float | None = None
        if baseline is not None and current is not None and baseline != 0:
            deviation_pct = round(((current - baseline) / baseline) * 100, 2)

        detected = self._is_threshold_breached(current, threshold, direction)
        if deviation_pct is not None and abs(deviation_pct) > 10.0 and not detected:
            detected = True

        severity = self._severity_for_deviation(deviation_pct, threshold, current)

        inputs_traced: list[str] = ["metric_name", "data_points", "baseline"]
        if inputs.source_id:
            inputs_traced.append(inputs.source_id)

        explanation = (
            f"baseline={baseline}, current={current}, "
            f"deviation={deviation_pct}%, threshold={threshold}"
        )

        return AnomalyReport(
            metric_name=inputs.metric_name or "unknown",
            baseline=baseline,
            current_value=current,
            threshold=threshold,
            direction=direction,
            deviation_pct=deviation_pct,
            severity=severity,
            detected=detected,
            explanation=explanation,
            formula="(current - baseline) / baseline * 100",
            inputs_traced=inputs_traced,
        )

    @staticmethod
    def _severity_for_deviation(
        deviation_pct: float | None,
        threshold: float | None,
        current: float | None,
    ) -> str:
        if current is None:
            return "unknown"
        if deviation_pct is None:
            return "low"
        abs_dev = abs(deviation_pct)
        if abs_dev > 50:
            return "critical"
        if abs_dev > 25:
            return "high"
        if abs_dev > 10:
            return "medium"
        return "low"

    def build_findings(self, report: AnomalyReport) -> list[AnomalyFinding]:
        """Derive a list of anomaly findings from a detected anomaly report."""
        if not report.detected:
            return []
        return [AnomalyFinding(
            metric=report.metric_name,
            value=report.current_value,
            baseline=report.baseline,
            threshold=report.threshold,
            direction=report.direction,
            severity=report.severity,
            explanation=report.explanation,
        )]


__all__ = ["ObservabilityAnalysisEngine"]
