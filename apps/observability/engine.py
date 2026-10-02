"""
Observability Capability Pack — Engine.
"""

from __future__ import annotations

import logging

from apps.observability.observability_engine import ObservabilityAnalysisEngine
from apps.observability.schemas import (
    BusinessContext,
    ObservabilityAnalystRequest,
    ObservabilityInputs,
    ObservabilityOperation,
    ObservabilityReport,
)

logger = logging.getLogger(__name__)


class ObservabilityAnalystEngine:
    """
    Orchestrates the observability analysis pipeline:
        1. Metrics Collection (thresholds + summaries)
        2. Trace Analysis (distributed tracing health)
        3. Log Analysis (pattern grouping)
        4. Anomaly Detection (baseline deviation)
    """

    def __init__(self) -> None:
        self.engine = ObservabilityAnalysisEngine()

    def execute(self, request: ObservabilityAnalystRequest) -> ObservabilityReport:
        inputs: ObservabilityInputs = request.inputs
        ctx: BusinessContext = request.business_context
        validation = self.engine.check_input_validation(inputs)

        limitations = [
            "Observability outputs are descriptive and do not replace operational runbooks",
            "Anomaly detection reflects observed signals, not root-cause diagnosis",
            "Threshold breaches require human validation before incident response",
        ]
        recommendations = [
            "Correlate metrics, traces, and logs before opening an incident",
            "Review alert thresholds against observed baselines regularly",
            "Preserve request source provenance for downstream triage",
        ]
        assumptions = []

        metric_summary = None
        trace_summary = None
        log_patterns = []
        anomaly_report = None
        findings = []
        source_reference_preserved = inputs.source_id is not None

        if not validation["valid"]:
            limitations.append(f"Input validation failed: {validation['validation_errors']}")
            if inputs.operation == ObservabilityOperation.metrics_collect:
                if inputs.metric_name is None:
                    limitations.append("metric_name is required to collect metrics")
            if inputs.operation == ObservabilityOperation.anomaly_detect:
                if inputs.baseline is None and not inputs.data_points:
                    limitations.append("baseline or data_points required for anomaly detection")

        if inputs.operation == ObservabilityOperation.metrics_collect:
            metric_summary = self.engine.collect_metrics(inputs)
            assumptions.extend(self._metric_assumptions(inputs))

        if inputs.operation == ObservabilityOperation.trace_analyze:
            trace_summary = self.engine.analyze_trace(inputs)

        if inputs.operation == ObservabilityOperation.log_analyze:
            log_patterns = self.engine.analyze_log(inputs)

        if inputs.operation == ObservabilityOperation.anomaly_detect:
            anomaly_report = self.engine.detect_anomaly(inputs)
            findings = self.engine.build_findings(anomaly_report)
            assumptions.append(f"baseline comparison for {ctx.project_name}")

        quality_score = 0.93 if validation["valid"] else 0.85

        return ObservabilityReport(
            request_id=request.request_id,
            operation=inputs.operation,
            metric_summary=metric_summary,
            trace_summary=trace_summary,
            log_patterns=log_patterns,
            anomaly_report=anomaly_report,
            findings=findings,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            source_reference_preserved=source_reference_preserved,
            anomaly_detection_claim=False,
            root_cause_attribution=False,
            quality_score=quality_score,
        )

    def _metric_assumptions(self, inputs: ObservabilityInputs) -> list[str]:
        """Surface the assumptions made for metric collection."""
        assumptions = []
        if inputs.aggregation:
            assumptions.append(f"aggregation={inputs.aggregation}")
        if inputs.time_window:
            assumptions.append(f"time_window={inputs.time_window}")
        if inputs.metric_type:
            assumptions.append(f"metric_type={inputs.metric_type}")
        if inputs.threshold is not None and inputs.threshold_direction:
            assumptions.append(
                f"threshold={inputs.threshold} ({inputs.threshold_direction})"
            )
        return assumptions


__all__ = ["ObservabilityAnalystEngine"]
