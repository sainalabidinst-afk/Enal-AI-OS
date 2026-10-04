from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from backend.app.core.telemetry.aggregator import aggregator

router = APIRouter()


@router.get("/metrics/analysis")
async def get_analysis_metrics():
    return aggregator.analysis_kpis()


@router.get("/metrics/chat")
async def get_chat_metrics():
    return aggregator.chat_kpis()


@router.get("/metrics/parser")
async def get_parser_metrics():
    return aggregator.parser_kpis()


@router.get("/metrics/reasoning")
async def get_reasoning_metrics():
    return aggregator.reasoning_kpis()


@router.get("/metrics/trading")
async def get_trading_metrics():
    return aggregator.trading_regime_kpis()


@router.get("/metrics/cross-pack")
async def get_cross_pack_metrics():
    return aggregator.cross_pack_correlation_kpis()


@router.get("/metrics/prometheus", response_class=PlainTextResponse)
async def get_prometheus_metrics():
    return aggregator.to_prometheus()


@router.get("/metrics/alerts")
async def get_alert_feeds():
    return {
        "trading_regime": [
            {
                "event_id": e["event_id"],
                "symbol": e["symbol"],
                "timeframe": e["timeframe"],
                "regime": e["regime"],
                "confidence": e["confidence"],
                "status": e["status"],
                "timestamp": e["timestamp"],
            }
            for e in aggregator._trading_regime_events[-50:]
        ],
        "cross_pack_correlations": [
            {
                "event_id": e["event_id"],
                "source_pack": e["source_pack"],
                "target_pack": e["target_pack"],
                "correlation_type": e["correlation_type"],
                "confidence": e["confidence"],
                "details": e["details"],
                "status": e["status"],
                "timestamp": e["timestamp"],
            }
            for e in aggregator._cross_pack_correlation_events[-50:]
        ],
    }


@router.get("/metrics")
async def get_all_metrics():
    return {
        "analysis": aggregator.analysis_kpis(),
        "chat": aggregator.chat_kpis(),
        "parser": aggregator.parser_kpis(),
        "reasoning": aggregator.reasoning_kpis(),
        "trading": aggregator.trading_regime_kpis(),
        "cross_pack": aggregator.cross_pack_correlation_kpis(),
    }
