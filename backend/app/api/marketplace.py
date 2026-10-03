"""
Marketplace API endpoints.

Provides endpoints for sharing, cloning, and discovering agents/tools.
"""

from __future__ import annotations

import logging
import time
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from backend.app.core.marketplace_service import marketplace_service

router = APIRouter()
logger = logging.getLogger(__name__)


class ShareRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    agent_id: str = ""
    visibility: str = "internal"
    allowed_roles: list[str] = []
    allow_clone: bool = True


class ShareResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    agent_id: str
    status: str
    created_at: str


class CloneRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    agent_id: str = ""
    target_project: str = "default"


class CloneResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    agent_id: str
    project: str
    cloned_at: str


class AnalyticsResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    agent_id: str
    clones: int
    views: int


@router.post("/marketplace/share", response_model=ShareResponse)
async def share_agent(request: ShareRequest):
    started = time.perf_counter()
    try:
        listing = marketplace_service.share(request.agent_id, request.model_dump())
        logger.info(
            "Shared agent %s in %.2fms",
            request.agent_id,
            (time.perf_counter() - started) * 1000,
        )
        return ShareResponse(**listing)
    except Exception as e:
        logger.error("Failed to share agent: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/marketplace/share/{agent_id}")
async def unshare_agent(agent_id: str):
    deleted = marketplace_service.unshare(agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"message": "Unshared"}


@router.get("/marketplace", response_model=list[ShareResponse])
async def list_marketplace():
    try:
        listings = marketplace_service.list_listings()
        return [ShareResponse(**listing) for listing in listings]
    except Exception as e:
        logger.error("Failed to list marketplace: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/marketplace/clone", response_model=CloneResponse)
async def clone_agent(request: CloneRequest):
    started = time.perf_counter()
    try:
        user_id = str(uuid.uuid4())
        marketplace_service.record_clone(request.agent_id, user_id)
        result = {
            "id": str(uuid.uuid4()),
            "agent_id": request.agent_id,
            "project": request.target_project,
            "cloned_at": datetime.now(UTC).isoformat(),
        }
        logger.info(
            "Cloned agent %s to %s in %.2fms",
            request.agent_id,
            request.target_project,
            (time.perf_counter() - started) * 1000,
        )
        return CloneResponse(**result)
    except Exception as e:
        logger.error("Failed to clone agent: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/marketplace/analytics/{agent_id}", response_model=AnalyticsResponse)
async def get_analytics(agent_id: str):
    analytics = marketplace_service.get_analytics(agent_id)
    return AnalyticsResponse(agent_id=agent_id, **analytics)
