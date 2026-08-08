"""
Capability Integration API
===========================

Endpoints:
- POST /api/v1/integration/trading-analysis
- POST /api/v1/integration/network-design-review
- POST /api/v1/integration/self-improvement
- GET /api/v1/integration/health
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/integration", tags=["integration"])


class TradingAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Trading pair, e.g. BTCUSDT", min_length=2, max_length=20)
    timeframes: list[str] | None = Field(
        default=None,
        description="Timeframes to analyze. Default: 15m, 1h, 4h, 1d",
    )
    exchange: str = Field(default="binance", description="Exchange name")


class NetworkDesignReviewRequest(BaseModel):
    topology_description: str = Field(
        ...,
        description="Network topology description",
        min_length=10,
    )
    requirements: str | None = Field(
        default=None,
        description="Network requirements",
    )


class SelfImprovementRequest(BaseModel):
    project_path: str = Field(
        ...,
        description="Path to the project to analyze",
        min_length=1,
    )
    analysis_type: str = Field(
        default="full",
        description="Type of analysis: full, security, performance, architecture",
    )


class IntegrationResponse(BaseModel):
    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None


def _workflow_result_to_response(result: Any) -> dict[str, Any]:
    context = getattr(result, "context", None)
    if context is None:
        return result.to_dict() if hasattr(result, "to_dict") else {}

    intermediate = getattr(context, "intermediate", {}) or {}
    evidences = getattr(context, "evidences", []) or []
    metadata = getattr(context, "metadata", {}) or {}

    reasoning_output = intermediate.get("reasoning_output", {})
    conclusions = (
        reasoning_output.get("conclusions", [])
        if isinstance(reasoning_output, dict)
        else []
    )

    legacy_reasoning_chain = metadata.get("legacy_reasoning_chain", [])
    if not legacy_reasoning_chain and conclusions:
        legacy_reasoning_chain = [f"Conclusion: {c}" for c in conclusions]

    return {
        "workflow_id": context.workflow_id,
        "workflow_type": context.workflow_type,
        "success": result.success,
        "result": {
            "inputs": dict(getattr(context, "inputs", {}) or {}),
            "outputs": dict(getattr(context, "outputs", {}) or {}),
            "intermediate": dict(intermediate),
            "reasoning_output": reasoning_output,
            "knowledge_context": intermediate.get("knowledge_context", {}),
        },
        "evidences": [e.to_dict() if hasattr(e, "to_dict") else e for e in evidences],
        "reasoning_chain": legacy_reasoning_chain,
        "knowledge_updates": [],
        "error": result.error,
        "started_at": result.started_at,
        "completed_at": result.completed_at,
        "latency_ms": result.latency_ms,
    }


@router.post("/trading-analysis", response_model=IntegrationResponse)
async def trading_analysis(req: TradingAnalysisRequest):
    """
    Integrated trading analysis with knowledge base and reasoning.

    Pipeline: Trading → Knowledge Query → Evidence Integration → Reasoning → Summary
    """
    try:
        from apps.integration.orchestrator import integration_engine

        result = await integration_engine.trading_analysis_with_knowledge(
            symbol=req.symbol,
            timeframes=req.timeframes,
            exchange=req.exchange,
        )

        return IntegrationResponse(
            success=result.success,
            data=_workflow_result_to_response(result),
            error=result.error,
        )
    except Exception as e:
        logger.exception("Trading analysis integration failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/network-design-review", response_model=IntegrationResponse)
async def network_design_review(req: NetworkDesignReviewRequest):
    """
    Integrated network design review with knowledge base and reasoning.

    Pipeline: Network → Knowledge Query → Reasoning → Design Review
    """
    try:
        from apps.integration.orchestrator import integration_engine

        result = await integration_engine.network_design_review_with_knowledge(
            topology_description=req.topology_description,
            requirements=req.requirements,
        )

        return IntegrationResponse(
            success=result.success,
            data=_workflow_result_to_response(result),
            error=result.error,
        )
    except Exception as e:
        logger.exception("Network design review integration failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/self-improvement", response_model=IntegrationResponse)
async def self_improvement_cycle(req: SelfImprovementRequest):
    """
    Self-improvement integration pipeline.

    Pipeline: Execution History → Knowledge Update → Proposal
    """
    try:
        from apps.integration.orchestrator import integration_engine

        result = await integration_engine.self_improvement_cycle(
            project_path=req.project_path,
            analysis_type=req.analysis_type,
        )

        return IntegrationResponse(
            success=result.success,
            data=_workflow_result_to_response(result),
            error=result.error,
        )
    except Exception as e:
        logger.exception("Self-improvement integration failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=dict[str, Any])
async def integration_health():
    """Health check for integration module."""
    return {
        "status": "ok",
        "module": "capability_integration",
        "version": "1.0.0",
        "workflows": [
            "trading_analysis_with_knowledge",
            "network_design_review_with_knowledge",
            "self_improvement_cycle",
        ],
    }
