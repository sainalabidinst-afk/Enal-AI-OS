from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class Aggregator:
    """Metrics aggregator for telemetry data."""

    _instance: Aggregator | None = None

    def __init__(self) -> None:
        self._chat_events: list[dict[str, Any]] = []
        self._analysis_events: list[dict[str, Any]] = []
        self._execution_events: list[dict[str, Any]] = []
        self._parser_events: list[dict[str, Any]] = []
        self._reasoning_events: list[dict[str, Any]] = []
        self._trading_regime_events: list[dict[str, Any]] = []
        self._cross_pack_correlation_events: list[dict[str, Any]] = []
        self._growth_alert_events: list[dict[str, Any]] = []

    def record_chat(
        self,
        chat_id: str,
        conversation_id: str,
        workspace_id: str,
        status: str,
        error: str | None,
        message_length: int,
        total_time_ms: float,
    ) -> None:
        self._chat_events.append(
            {
                "chat_id": chat_id,
                "conversation_id": conversation_id,
                "workspace_id": workspace_id,
                "status": status,
                "error": error,
                "message_length": message_length,
                "total_time_ms": total_time_ms,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_analysis(
        self,
        analysis_id: str,
        status: str,
        error: str | None,
        workspace_id: str,
        vendor: str,
        device_type: str,
        files: int,
        size_bytes: int,
        parser: str,
        total_time_ms: float,
        findings: int,
        confidence: float,
        compliance_score: float | None,
        executive_report: bool,
        benchmark_case_id: str | None,
    ) -> None:
        self._analysis_events.append(
            {
                "analysis_id": analysis_id,
                "status": status,
                "error": error,
                "workspace_id": workspace_id,
                "vendor": vendor,
                "device_type": device_type,
                "files": files,
                "size_bytes": size_bytes,
                "parser": parser,
                "total_time_ms": total_time_ms,
                "findings": findings,
                "confidence": confidence,
                "compliance_score": compliance_score,
                "executive_report": executive_report,
                "benchmark_case_id": benchmark_case_id,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_execution(
        self, execution_id: str, status: str, goal: str, error: str | None, total_time_ms: float
    ) -> None:  # noqa: E501
        self._execution_events.append(
            {
                "execution_id": execution_id,
                "status": status,
                "goal": goal,
                "error": error,
                "total_time_ms": total_time_ms,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_parser(self, attachment_id: str, success: bool, format_detected: str | None) -> None:
        self._parser_events.append(
            {
                "attachment_id": attachment_id,
                "success": success,
                "format_detected": format_detected,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_reasoning(
        self, query_id: str, step_count: int, success: bool, duration_ms: float
    ) -> None:  # noqa: E501
        self._reasoning_events.append(
            {
                "query_id": query_id,
                "step_count": step_count,
                "success": success,
                "duration_ms": duration_ms,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_trading_regime(
        self,
        event_id: str,
        symbol: str,
        timeframe: str,
        regime: str,
        confidence: float,
        volatility: str = "",
        trend_strength: float = 0.0,
        source: str = "live",
        status: str = "success",
        error: str | None = None,
    ) -> None:
        self._trading_regime_events.append(
            {
                "event_id": event_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "regime": regime,
                "confidence": confidence,
                "volatility": volatility,
                "trend_strength": trend_strength,
                "source": source,
                "status": status,
                "error": error,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_cross_pack_correlation(
        self,
        event_id: str,
        source_pack: str,
        target_pack: str,
        correlation_type: str,
        confidence: float,
        details: str = "",
        status: str = "warning",
        error: str | None = None,
    ) -> None:
        self._cross_pack_correlation_events.append(
            {
                "event_id": event_id,
                "source_pack": source_pack,
                "target_pack": target_pack,
                "correlation_type": correlation_type,
                "confidence": confidence,
                "details": details,
                "status": status,
                "error": error,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def record_growth_alert(
        self,
        event_id: str,
        alert_type: str,
        severity: str,
        subject: str,
        message: str,
        details: dict[str, Any] | None = None,
        status: str = "open",
        source: str = "self_development",
    ) -> None:
        """Record a habit / goal-drift alert for the main dashboard feed."""
        self._growth_alert_events.append(
            {
                "event_id": event_id,
                "alert_type": alert_type,
                "severity": severity,
                "subject": subject,
                "message": message,
                "details": details or {},
                "status": status,
                "source": source,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )
        if len(self._growth_alert_events) > 500:
            self._growth_alert_events = self._growth_alert_events[-500:]

    def analysis_kpis(self) -> dict[str, Any]:
        events = self._analysis_events
        if not events:
            return {"total_analyses": 0, "avg_findings": 0.0, "avg_risk_score": 0.0}
        return {
            "total_analyses": len(events),
            "avg_findings": round(sum(e["findings"] for e in events) / len(events), 2),
            "avg_risk_score": round(
                sum(e["compliance_score"] for e in events if e["compliance_score"] is not None)
                / max(len([e for e in events if e["compliance_score"] is not None]), 1),  # noqa: E501
                2,
            ),
        }

    def chat_kpis(self) -> dict[str, Any]:
        events = self._chat_events
        if not events:
            return {"total_messages": 0, "avg_latency_ms": 0.0}
        return {
            "total_messages": sum(e["message_length"] for e in events),
            "avg_latency_ms": round(
                sum(e["total_time_ms"] for e in events) / max(len(events), 1), 2
            ),  # noqa: E501
        }

    def parser_kpis(self) -> dict[str, Any]:
        events = self._parser_events
        if not events:
            return {"total_parses": 0, "success_rate": 0.0}
        success_count = sum(1 for e in events if e["success"])
        return {
            "total_parses": len(events),
            "success_rate": round(success_count / max(len(events), 1), 2),
        }

    def reasoning_kpis(self) -> dict[str, Any]:
        events = self._reasoning_events
        if not events:
            return {"total_queries": 0, "avg_steps": 0.0, "avg_duration_ms": 0.0}
        return {
            "total_queries": len(events),
            "avg_steps": round(sum(e["step_count"] for e in events) / len(events), 2),
            "avg_duration_ms": round(sum(e["duration_ms"] for e in events) / len(events), 2),
        }

    def trading_regime_kpis(self) -> dict[str, Any]:
        events = self._trading_regime_events
        if not events:
            return {
                "total_regime_checks": 0,
                "avg_confidence": 0.0,
                "low_confidence_count": 0,
                "regime_distribution": {},
            }
        low_confidence = sum(1 for e in events if e["confidence"] < 0.5)
        regime_distribution: dict[str, int] = {}
        for e in events:
            regime_distribution[e["regime"]] = regime_distribution.get(e["regime"], 0) + 1
        return {
            "total_regime_checks": len(events),
            "avg_confidence": round(sum(e["confidence"] for e in events) / len(events), 4),
            "low_confidence_count": low_confidence,
            "regime_distribution": regime_distribution,
        }

    def cross_pack_correlation_kpis(self) -> dict[str, Any]:
        events = self._cross_pack_correlation_events
        if not events:
            return {"total_correlations": 0, "by_type": {}, "avg_confidence": 0.0}
        by_type: dict[str, int] = {}
        for e in events:
            by_type[e["correlation_type"]] = by_type.get(e["correlation_type"], 0) + 1
        return {
            "total_correlations": len(events),
            "by_type": by_type,
            "avg_confidence": round(sum(e["confidence"] for e in events) / len(events), 4),
        }

    def growth_alert_kpis(self) -> dict[str, Any]:
        events = self._growth_alert_events
        if not events:
            return {
                "total_growth_alerts": 0,
                "by_type": {},
                "by_severity": {},
            }
        by_type: dict[str, int] = {}
        by_severity: dict[str, int] = {}
        for e in events:
            by_type[e["alert_type"]] = by_type.get(e["alert_type"], 0) + 1
            by_severity[e["severity"]] = by_severity.get(e["severity"], 0) + 1
        return {
            "total_growth_alerts": len(events),
            "by_type": by_type,
            "by_severity": by_severity,
        }

    def to_prometheus(self) -> str:
        """Export metrics in Prometheus text format."""
        lines: list[str] = []
        analysis_kpis = self.analysis_kpis()
        chat_kpis = self.chat_kpis()
        parser_kpis = self.parser_kpis()
        reasoning_kpis = self.reasoning_kpis()
        trading_kpis = self.trading_regime_kpis()
        correlation_kpis = self.cross_pack_correlation_kpis()

        lines.append("# HELP ecp_analysis_total Total number of analyses")
        lines.append("# TYPE ecp_analysis_total gauge")
        lines.append(f"ecp_analysis_total {analysis_kpis['total_analyses']}")
        lines.append("# HELP ecp_analysis_avg_findings Average findings per analysis")
        lines.append("# TYPE ecp_analysis_avg_findings gauge")
        lines.append(f"ecp_analysis_avg_findings {analysis_kpis['avg_findings']}")
        lines.append("# HELP ecp_chat_total Total chat messages")
        lines.append("# TYPE ecp_chat_total gauge")
        lines.append(f"ecp_chat_total {chat_kpis['total_messages']}")
        lines.append("# HELP ecp_chat_avg_latency_ms Average chat latency in ms")
        lines.append("# TYPE ecp_chat_avg_latency_ms gauge")
        lines.append(f"ecp_chat_avg_latency_ms {chat_kpis['avg_latency_ms']}")
        lines.append("# HELP ecp_parser_success_rate Parser success rate")
        lines.append("# TYPE ecp_parser_success_rate gauge")
        lines.append(f"ecp_parser_success_rate {parser_kpis['success_rate']}")
        lines.append("# HELP ecp_reasoning_total Total reasoning queries")
        lines.append("# TYPE ecp_reasoning_total gauge")
        lines.append(f"ecp_reasoning_total {reasoning_kpis['total_queries']}")
        lines.append("# HELP ecp_trading_regime_checks_total Total trading regime checks")
        lines.append("# TYPE ecp_trading_regime_checks_total gauge")
        lines.append(f"ecp_trading_regime_checks_total {trading_kpis['total_regime_checks']}")
        lines.append("# HELP ecp_trading_regime_avg_confidence Average trading regime confidence")
        lines.append("# TYPE ecp_trading_regime_avg_confidence gauge")
        lines.append(f"ecp_trading_regime_avg_confidence {trading_kpis['avg_confidence']}")
        lines.append("# HELP ecp_trading_low_confidence_total Low confidence trading regime count")
        lines.append("# TYPE ecp_trading_low_confidence_total gauge")
        lines.append(f"ecp_trading_low_confidence_total {trading_kpis['low_confidence_count']}")
        lines.append("# HELP ecp_cross_pack_correlations_total Cross-pack correlations detected")
        lines.append("# TYPE ecp_cross_pack_correlations_total gauge")
        lines.append(f"ecp_cross_pack_correlations_total {correlation_kpis['total_correlations']}")

        growth_kpis = self.growth_alert_kpis()
        lines.append("# HELP ecp_growth_alerts_total Growth alerts (habit / goal drift)")
        lines.append("# TYPE ecp_growth_alerts_total gauge")
        lines.append(f"ecp_growth_alerts_total {growth_kpis['total_growth_alerts']}")

        return "\n".join(lines) + "\n"


aggregator = Aggregator()
