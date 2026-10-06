"""
Digital Twin API Endpoints
============================

Endpoints:
- POST /api/v1/twin/simulate — run a scenario simulation
- POST /api/v1/twin/red-team — run adversarial red team test
- POST /api/v1/twin/causal-trace — run causal trace analysis
- GET  /api/v1/twin/status — get digital twin status
- GET  /api/v1/twin/audit — get recent adversarial audit results
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/twin", tags=["digital-twin"])


# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------


class SimulateRequest(BaseModel):
    """Request body for scenario simulation."""

    scenario: str = Field(..., description="Natural language scenario description")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Simulation parameters")
    iterations: int = Field(default=100, ge=1, le=10000, description="Monte Carlo iterations")


class RedTeamRequest(BaseModel):
    """Request body for red team adversarial test."""

    subject: str = Field(..., description="The plan/strategy/recommendation to attack")
    subject_type: str = Field(default="plan", description="Type of subject")


class CausalTraceRequest(BaseModel):
    """Request body for causal trace analysis."""

    treatment: str = Field(..., description="Treatment variable (cause)")
    outcome: str = Field(..., description="Outcome variable (effect)")
    conditions: dict[str, Any] = Field(default_factory=dict, description="Controlling conditions")


class MirrorRequest(BaseModel):
    """Request body for state mirroring."""

    system_state: dict[str, Any] = Field(
        default_factory=dict, description="Real-world system state to mirror"
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/simulate")
async def simulate(req: SimulateRequest):
    """
    Run a scenario simulation on the digital twin.

    Orchestrates ScenarioSimulatorEngine with the provided scenario and parameters.
    """
    try:
        from apps.digital_twin_engine.engine import DigitalTwinEngine

        engine = DigitalTwinEngine()
        result = engine.run_simulation(
            scenario=req.scenario,
            parameters=req.parameters,
            iterations=req.iterations,
        )
        return result.model_dump()
    except Exception as exc:
        logger.exception("Simulation failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/red-team")
async def red_team(req: RedTeamRequest):
    """
    Run a red team adversarial test against a subject.

    Orchestrates AdversarialTestingEngine to find vulnerabilities and hardening paths.
    """
    try:
        from apps.digital_twin_engine.engine import DigitalTwinEngine

        engine = DigitalTwinEngine()
        result = engine.run_red_team(subject=req.subject, subject_type=req.subject_type)
        return result.model_dump()
    except Exception as exc:
        logger.exception("Red team audit failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/causal-trace")
async def causal_trace(req: CausalTraceRequest):
    """
    Run a causal trace analysis on the digital twin.

    Orchestrates CrossDomainGraphEngine for causal inference and counterfactual analysis.
    """
    try:
        from apps.digital_twin_engine.engine import DigitalTwinEngine

        engine = DigitalTwinEngine()
        result = engine.run_causal_trace(
            treatment=req.treatment,
            outcome=req.outcome,
            conditions=req.conditions,
        )
        return result.model_dump()
    except Exception as exc:
        logger.exception("Causal trace failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/mirror")
async def mirror_state(req: MirrorRequest):
    """
    Mirror real-world system state into the digital twin.

    Creates or updates the TwinState with the provided system state.
    """
    try:
        from apps.digital_twin_engine.engine import DigitalTwinEngine

        engine = DigitalTwinEngine()
        twin = engine.mirror_state(req.system_state)
        return twin.model_dump()
    except Exception as exc:
        logger.exception("State mirroring failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/status")
async def twin_status():
    """
    Get the current digital twin status.

    Returns twin health, active simulations, pending tests, and sync info.
    """
    try:
        from apps.digital_twin_engine.engine import DigitalTwinEngine

        engine = DigitalTwinEngine()
        status = engine.get_status()
        return status.model_dump()
    except Exception as exc:
        logger.exception("Status retrieval failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/audit")
async def audit_history():
    """
    Get recent adversarial audit results.

    Returns the history of red team audits performed by this twin instance.
    """
    try:
        from apps.digital_twin_engine.engine import DigitalTwinEngine

        engine = DigitalTwinEngine()
        status = engine.get_status()
        return {
            "twin_id": status.twin_id,
            "audit_history_count": status.audit_history_count,
            "audits": engine._audit_history,
        }
    except Exception as exc:
        logger.exception("Audit retrieval failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
