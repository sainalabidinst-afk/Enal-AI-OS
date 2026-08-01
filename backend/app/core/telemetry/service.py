from __future__ import annotations

import logging
from typing import Any

from .aggregator import aggregator

logger = logging.getLogger(__name__)


def record_chat_event(
    chat_id: str,
    conversation_id: str,
    workspace_id: str,
    status: str = "success",
    error: str | None = None,
    message_length: int = 0,
    total_time_ms: float = 0.0,
) -> None:
    aggregator.record_chat(
        chat_id=chat_id,
        conversation_id=conversation_id,
        workspace_id=workspace_id,
        status=status,
        error=error,
        message_length=message_length,
        total_time_ms=total_time_ms,
    )


def record_analysis_event(
    analysis_id: str,
    status: str = "success",
    error: str | None = None,
    workspace_id: str = "",
    vendor: str = "",
    device_type: str = "",
    files: int = 1,
    size_bytes: int = 0,
    parser: str = "",
    total_time_ms: float = 0.0,
    findings: int = 0,
    confidence: float = 0.0,
    compliance_score: float | None = None,
    executive_report: bool = False,
    benchmark_case_id: str | None = None,
) -> None:
    aggregator.record_analysis(
        analysis_id=analysis_id,
        status=status,
        error=error,
        workspace_id=workspace_id,
        vendor=vendor,
        device_type=device_type,
        files=files,
        size_bytes=size_bytes,
        parser=parser,
        total_time_ms=total_time_ms,
        findings=findings,
        confidence=confidence,
        compliance_score=compliance_score,
        executive_report=executive_report,
        benchmark_case_id=benchmark_case_id,
    )


def record_execution_event(
    execution_id: str,
    status: str,
    goal: str,
    error: str | None = None,
    total_time_ms: float = 0.0,
) -> None:
    aggregator.record_execution(
        execution_id=execution_id,
        status=status,
        goal=goal,
        error=error,
        total_time_ms=total_time_ms,
    )


def get_metrics() -> dict[str, Any]:
    return {
        "analysis": aggregator.analysis_kpis(),
        "chat": aggregator.chat_kpis(),
        "parser": aggregator.parser_kpis(),
        "reasoning": aggregator.reasoning_kpis(),
    }