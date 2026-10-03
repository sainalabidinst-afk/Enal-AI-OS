"""
Guardrail API endpoints.

Provides endpoints for testing guardrails and managing policies.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from backend.app.core.guardrail_engine import CorrectiveAction, guardrail_engine

router = APIRouter()
logger = logging.getLogger(__name__)


class GuardrailTestRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    content: str = ""
    guardrails: dict[str, bool] = {}


class GuardrailTestResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[dict[str, Any]]
    triggered_count: int
    total_checked: int


@router.post("/guardrails/test", response_model=GuardrailTestResponse)
async def test_guardrails(request: GuardrailTestRequest):
    try:
        results = guardrail_engine.check(request.content, request.guardrails)
        triggered = [r for r in results if r.triggered]
        return GuardrailTestResponse(
            results=[
                {
                    "guardrail": r.guardrail,
                    "triggered": r.triggered,
                    "action": (
                        r.action.value
                        if isinstance(r.action, CorrectiveAction)
                        else str(r.action)
                    ),
                    "details": r.details,
                    "modified_content": r.modified_content,
                }
                for r in results
            ],
            triggered_count=len(triggered),
            total_checked=len(results),
        )
    except Exception as e:
        logger.error("Guardrail test failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/guardrails")
async def list_guardrails():
    return {
        "guardrails": [
            {"name": "pii", "description": "Detect PII (email, phone, SSN, credit card)"},
            {"name": "toxic_language", "description": "Detect toxic content"},
            {"name": "prompt_injection", "description": "Detect injection attacks"},
            {"name": "bias_check", "description": "Detect bias in output"},
            {"name": "logic_check", "description": "Validate logical consistency"},
            {"name": "competitor_check", "description": "Detect competitor mentions"},
            {"name": "gibberish", "description": "Detect nonsense output"},
            {"name": "reading_level", "description": "Validate reading complexity"},
        ]
    }
