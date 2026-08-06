from __future__ import annotations

import logging
from typing import Any
from datetime import UTC, datetime

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

    def record_execution(self, execution_id: str, status: str, goal: str, error: str | None, total_time_ms: float) -> None:
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

    def record_reasoning(self, query_id: str, step_count: int, success: bool, duration_ms: float) -> None:
        self._reasoning_events.append(
            {
                "query_id": query_id,
                "step_count": step_count,
                "success": success,
                "duration_ms": duration_ms,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def analysis_kpis(self) -> dict[str, Any]:
        events = self._analysis_events
        if not events:
            return {"total_analyses": 0, "avg_findings": 0.0, "avg_risk_score": 0.0}
        return {
            "total_analyses": len(events),
            "avg_findings": round(sum(e["findings"] for e in events) / len(events), 2),
            "avg_risk_score": round(
                sum(e["compliance_score"] for e in events if e["compliance_score"] is not None) / max(len([e for e in events if e["compliance_score"] is not None]), 1),
                2,
            ),
        }

    def chat_kpis(self) -> dict[str, Any]:
        events = self._chat_events
        if not events:
            return {"total_messages": 0, "avg_latency_ms": 0.0}
        return {
            "total_messages": sum(e["message_length"] for e in events),
            "avg_latency_ms": round(sum(e["total_time_ms"] for e in events) / max(len(events), 1), 2),
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


aggregator = Aggregator()