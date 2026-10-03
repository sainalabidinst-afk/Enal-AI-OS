"""
End-to-End Scenario API endpoints.

Provides endpoints for Data Visualization, NLU Intent Recognition,
Policy Enforcement (GDPR/ISO), and Dashboard Update.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.app.core.dashboard_updater import dashboard_updater
from backend.app.core.data_visualization import data_visualization
from backend.app.core.nlu_service import nlu_service
from backend.app.core.policy_enforcement import policy_enforcement

router = APIRouter()
logger = logging.getLogger(__name__)


class VisualizationRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    data: dict[str, Any] = Field(default_factory=dict)
    chart_type: str = "line"
    title: str = ""


class VisualizationResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    charts: list[dict[str, Any]] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""
    quality_score: float = 0.0


class NLURequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str = ""


class NLUResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    intent: str = ""
    confidence: float = 0.0
    entities: list[dict[str, Any]] = Field(default_factory=list)
    fallback_intent: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class PolicyCheckRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    action: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)


class PolicyCheckResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    overall_status: str = "pass"
    risk_score: float = 0.0
    framework: str = ""
    checks: list[dict[str, Any]] = Field(default_factory=list)
    timestamp: str = ""
    quality_score: float = 0.0


class DashboardUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    execution_id: str = ""
    steps: list[str] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)


class DashboardUpdateResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    execution_id: str = ""
    status: str = "running"
    current_step: str = ""
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""
    quality_score: float = 0.0


@router.post("/visualization/generate", response_model=VisualizationResponse)
async def generate_visualization(request: VisualizationRequest):
    """Generate a data visualization (chart) from data."""
    started = time.perf_counter()
    try:
        report = data_visualization.generate_report(
            data=request.data,
            chart_type=request.chart_type,
            title=request.title,
        )
        logger.info("Generated visualization in %.2fms", (time.perf_counter() - started) * 1000)
        return VisualizationResponse(
            charts=[c.model_dump() for c in report.charts],
            artifacts=report.artifacts,
            summary=report.summary,
            quality_score=report.quality_score,
        )
    except Exception as e:
        logger.error("Visualization generation failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/nlu/classify", response_model=NLUResponse)
async def classify_intent(request: NLURequest):
    """Classify user intent from text."""
    started = time.perf_counter()
    try:
        result = nlu_service.classify(request.text)
        logger.info("Classified intent in %.2fms", (time.perf_counter() - started) * 1000)
        return NLUResponse(
            intent=result.intent,
            confidence=result.confidence,
            entities=result.entities,
            fallback_intent=result.fallback_intent,
            parameters=result.parameters,
        )
    except Exception as e:
        logger.error("NLU classification failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/nlu/intents")
async def list_supported_intents():
    """Return list of supported NLU intents."""
    return {"intents": nlu_service.get_supported_intents()}


@router.post("/policy/check", response_model=PolicyCheckResponse)
async def check_policy(request: PolicyCheckRequest):
    """Run GDPR/ISO policy checks for an action and payload."""
    started = time.perf_counter()
    try:
        report = policy_enforcement.check_action(request.action, request.payload)
        logger.info("Policy check completed in %.2fms", (time.perf_counter() - started) * 1000)
        return PolicyCheckResponse(
            overall_status=report.overall_status,
            risk_score=report.risk_score,
            framework=report.framework,
            checks=[c.model_dump() for c in report.checks],
            timestamp=report.timestamp.isoformat(),
            quality_score=report.quality_score,
        )
    except Exception as e:
        logger.error("Policy check failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/policy/policies")
async def list_policies():
    """Return list of supported policy IDs."""
    return {"policies": policy_enforcement.get_supported_policies()}


@router.post("/dashboard/update", response_model=DashboardUpdateResponse)
async def update_dashboard(request: DashboardUpdateRequest):
    """Create a dashboard update with execution timeline and artifacts."""
    started = time.perf_counter()
    try:
        update = dashboard_updater.create_update(
            execution_id=request.execution_id,
            steps=request.steps,
            artifacts=request.artifacts,
        )
        logger.info("Dashboard update created in %.2fms", (time.perf_counter() - started) * 1000)
        return DashboardUpdateResponse(
            execution_id=update.execution_id,
            status=update.status,
            current_step=update.current_step,
            timeline=[t.model_dump() for t in update.timeline],
            artifacts=[a.model_dump() for a in update.artifacts],
            summary=update.summary,
            quality_score=update.quality_score,
        )
    except Exception as e:
        logger.error("Dashboard update failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/dashboard/artifacts/append")
async def append_dashboard_artifact(
    execution_id: str,
    artifact: dict[str, Any],
):
    """Append a new artifact to an existing dashboard update."""
    try:
        # Retrieve existing update from in-memory store or create a new one
        update = dashboard_updater.create_update(
            execution_id=execution_id,
            steps=[],
            artifacts=[artifact],
        )
        return {"message": "Artifact appended", "artifact_count": len(update.artifacts)}
    except Exception as e:
        logger.error("Failed to append dashboard artifact: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
