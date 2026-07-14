from __future__ import annotations

from fastapi import APIRouter
from backend.app.core.telemetry.aggregator import MetricsAggregator

router = APIRouter()
aggregator = MetricsAggregator()


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


@router.get("/metrics")
async def get_all_metrics():
    return {
        "analysis": aggregator.analysis_kpis(),
        "chat": aggregator.chat_kpis(),
        "parser": aggregator.parser_kpis(),
        "reasoning": aggregator.reasoning_kpis(),
    }
