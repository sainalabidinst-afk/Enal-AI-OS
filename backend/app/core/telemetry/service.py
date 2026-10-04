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
        "trading": aggregator.trading_regime_kpis(),
        "cross_pack": aggregator.cross_pack_correlation_kpis(),
    }


def record_trading_regime_event(
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
    aggregator.record_trading_regime(
        event_id=event_id,
        symbol=symbol,
        timeframe=timeframe,
        regime=regime,
        confidence=confidence,
        volatility=volatility,
        trend_strength=trend_strength,
        source=source,
        status=status,
        error=error,
    )


def record_cross_pack_correlation_event(
    event_id: str,
    source_pack: str,
    target_pack: str,
    correlation_type: str,
    confidence: float,
    details: str = "",
    status: str = "warning",
    error: str | None = None,
) -> None:
    aggregator.record_cross_pack_correlation(
        event_id=event_id,
        source_pack=source_pack,
        target_pack=target_pack,
        correlation_type=correlation_type,
        confidence=confidence,
        details=details,
        status=status,
        error=error,
    )
