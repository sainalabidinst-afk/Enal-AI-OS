"""
Blueprint API endpoints for visual builder.

Provides CRUD operations for agent and tool blueprints.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from backend.app.core.blueprint_repository import blueprint_repository
from backend.app.core.schemas import AgentBlueprint, ToolBlueprint

router = APIRouter()
logger = logging.getLogger(__name__)


class CreateAgentBlueprintRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = ""
    description: str = ""
    model: str = "gpt-4o"
    tools: list[str] = []
    knowledge_base_ids: list[str] = []
    prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 1024
    metadata: dict[str, Any] = {}


class CreateToolBlueprintRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = ""
    description: str = ""
    steps: list[dict[str, Any]] = []
    branches: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {}


class BlueprintResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str = ""
    description: str = ""
    model: str = ""
    tools: list[str] = []
    knowledge_base_ids: list[str] = []
    prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 1024
    metadata: dict[str, Any] = {}
    created_at: str = ""
    updated_at: str = ""


@router.post("/blueprints/agent", response_model=BlueprintResponse)
async def create_agent_blueprint(request: CreateAgentBlueprintRequest):
    started = time.perf_counter()
    try:
        blueprint = AgentBlueprint(**request.model_dump())
        result = blueprint_repository.create_agent(blueprint.model_dump())
        logger.info(
            "Created agent blueprint %s in %.2fms",
            result.get("id"),
            (time.perf_counter() - started) * 1000,
        )
        return BlueprintResponse(**result)
    except Exception as e:
        logger.error("Failed to create agent blueprint: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/blueprints/agent", response_model=list[BlueprintResponse])
async def list_agent_blueprints():
    try:
        blueprints = blueprint_repository.list_agents()
        return [BlueprintResponse(**bp) for bp in blueprints]
    except Exception as e:
        logger.error("Failed to list agent blueprints: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/blueprints/agent/{blueprint_id}", response_model=BlueprintResponse)
async def get_agent_blueprint(blueprint_id: str):
    blueprint = blueprint_repository.get_agent(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return BlueprintResponse(**blueprint)


@router.put("/blueprints/agent/{blueprint_id}", response_model=BlueprintResponse)
async def update_agent_blueprint(blueprint_id: str, request: CreateAgentBlueprintRequest):
    existing = blueprint_repository.get_agent(blueprint_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    try:
        updated = blueprint_repository.update_agent(blueprint_id, request.model_dump())
        assert updated is not None
        return BlueprintResponse(**updated)
    except Exception as e:
        logger.error("Failed to update agent blueprint %s: %s", blueprint_id, e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/blueprints/agent/{blueprint_id}")
async def delete_agent_blueprint(blueprint_id: str):
    deleted = blueprint_repository.delete_agent(blueprint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return {"message": "Deleted"}


@router.post("/blueprints/tool", response_model=BlueprintResponse)
async def create_tool_blueprint(request: CreateToolBlueprintRequest):
    started = time.perf_counter()
    try:
        blueprint = ToolBlueprint(**request.model_dump())
        result = blueprint_repository.create_tool(blueprint.model_dump())
        logger.info(
            "Created tool blueprint %s in %.2fms",
            result.get("id"),
            (time.perf_counter() - started) * 1000,
        )
        return BlueprintResponse(**result)
    except Exception as e:
        logger.error("Failed to create tool blueprint: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/blueprints/tool", response_model=list[BlueprintResponse])
async def list_tool_blueprints():
    try:
        blueprints = blueprint_repository.list_tools()
        return [BlueprintResponse(**bp) for bp in blueprints]
    except Exception as e:
        logger.error("Failed to list tool blueprints: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/blueprints/tool/{blueprint_id}", response_model=BlueprintResponse)
async def get_tool_blueprint(blueprint_id: str):
    blueprint = blueprint_repository.get_tool(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return BlueprintResponse(**blueprint)


@router.put("/blueprints/tool/{blueprint_id}", response_model=BlueprintResponse)
async def update_tool_blueprint(blueprint_id: str, request: CreateToolBlueprintRequest):
    existing = blueprint_repository.get_tool(blueprint_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    try:
        updated = blueprint_repository.update_tool(blueprint_id, request.model_dump())
        assert updated is not None
        return BlueprintResponse(**updated)
    except Exception as e:
        logger.error("Failed to update tool blueprint %s: %s", blueprint_id, e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/blueprints/tool/{blueprint_id}")
async def delete_tool_blueprint(blueprint_id: str):
    deleted = blueprint_repository.delete_tool(blueprint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return {"message": "Deleted"}


@router.get("/blueprints/{kind}/{blueprint_id}/dependencies")
async def resolve_dependencies(kind: str, blueprint_id: str):
    if kind not in ("agent", "tool"):
        raise HTTPException(status_code=400, detail="kind must be 'agent' or 'tool'")
    result = blueprint_repository.resolve_dependencies(blueprint_id, kind=kind)
    return result
