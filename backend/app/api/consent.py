"""
Consent & Safety API endpoints
==============================

Provides endpoints for Jenny's consent/permission flow:
- POST /consent/request — create a consent request (called by action layer)
- POST /consent/respond — approve or deny a request
- GET /consent/pending — list pending requests for user
- GET /consent/history — view consent history

ADR-025: Consent & Permission Architecture
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from backend.app.core.consent import (
    ConsentStatus,
    RiskLevel,
    classify_risk,
    consent_manager,
)

router = APIRouter()


@router.post("/request", response_model=dict[str, Any])
async def request_consent(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a consent request for a potentially risky action.

    Expected payload fields:
        - action_type: str  — the action to be performed
        - description: str  — human-readable description
        - params: dict     — action parameters (optional)
        - session_id: str  — originating session (optional)
        - connector_type: str — connector name (optional)
        - timeout_seconds: int — override default timeout (optional)
    """
    action_type = payload.get("action_type", "")
    description = payload.get("description", "")

    if not action_type:
        raise HTTPException(status_code=400, detail="action_type is required")

    if not description:
        description = f"Allow '{action_type}' action?"

    params = payload.get("params", {})
    session_id = payload.get("session_id", "")
    connector_type = payload.get("connector_type", "")
    timeout = payload.get("timeout_seconds")

    request = consent_manager.request(
        action_type=action_type,
        description=description,
        params=params,
        session_id=session_id,
        connector_type=connector_type,
        timeout_seconds=timeout,
    )

    return {
        "request_id": request.request_id,
        "status": request.status.value,
        "risk_level": request.risk_level.value,
        "description": request.description,
        "timeout_seconds": request.timeout_seconds,
        "expires_at": request.expires_at.isoformat(),
    }


@router.post("/respond", response_model=dict[str, Any])
async def respond_consent(payload: dict[str, Any]) -> dict[str, Any]:
    """Approve or deny a consent request.

    Expected payload fields:
        - request_id: str  — the consent request ID
        - decision: str    — 'approve' or 'deny'
        - responder: str   — who is responding (optional, default 'user')
    """
    request_id = payload.get("request_id", "")
    decision = payload.get("decision", "").lower()
    responder = payload.get("responder", "user")

    if not request_id:
        raise HTTPException(status_code=400, detail="request_id is required")

    if decision == "approve":
        request = consent_manager.approve(request_id, responder)
    elif decision == "deny":
        request = consent_manager.deny(request_id, responder)
    else:
        raise HTTPException(
            status_code=400,
            detail="decision must be 'approve' or 'deny'",
        )

    if request is None:
        raise HTTPException(status_code=404, detail="Consent request not found")

    return {
        "request_id": request.request_id,
        "status": request.status.value,
        "responder": request.responder,
        "response_at": request.response_at.isoformat() if request.response_at else None,
    }


@router.get("/pending", response_model=list[dict[str, Any]])
async def list_pending_consents() -> list[dict[str, Any]]:
    """List all pending consent requests (not expired)."""
    results = []
    for r in consent_manager._requests.values():
        if r.status == ConsentStatus.PENDING and not r.is_expired:
            results.append({
                "request_id": r.request_id,
                "action_type": r.action_type,
                "description": r.description,
                "risk_level": r.risk_level.value,
                "created_at": r.created_at.isoformat(),
                "expires_at": r.expires_at.isoformat(),
            })
    return results


@router.get("/history", response_model=list[dict[str, Any]])
async def get_consent_history(
    status: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """View consent request history, optionally filtered by status."""
    status_filter = None
    if status:
        try:
            status_filter = ConsentStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {status}. Use: pending, approved, denied, expired",
            )

    history = consent_manager.get_history(status=status_filter, limit=limit)
    return [
        {
            "request_id": r.request_id,
            "session_id": r.session_id,
            "action_type": r.action_type,
            "description": r.description,
            "risk_level": r.risk_level.value,
            "status": r.status.value,
            "connector_type": r.connector_type,
            "created_at": r.created_at.isoformat(),
            "response_at": r.response_at.isoformat() if r.response_at else None,
            "responder": r.responder,
        }
        for r in history
    ]


@router.get("/classify", response_model=dict[str, Any])
async def classify_action(
    action_type: str,
    connector_type: str | None = None,
) -> dict[str, Any]:
    """Classify an action by risk level without creating a consent request."""
    params = {"connector_type": connector_type or ""}
    risk = classify_risk(action_type, params)
    return {
        "action_type": action_type,
        "risk_level": risk.value,
        "requires_consent": risk in (RiskLevel.MEDIUM, RiskLevel.HIGH),
    }


@router.on_event("startup")
async def start_consent_cleanup() -> None:
    """Run cleanup on startup to clear stale consent requests."""
    consent_manager.cleanup()
