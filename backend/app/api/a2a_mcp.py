"""
A2A/MCP API endpoints.

Provides endpoints for managing external A2A agents and MCP servers.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from backend.app.core.a2a_invoker import a2a_invoker
from backend.app.core.a2a_registry import a2a_registry
from backend.app.core.mcp_tool_proxy import mcp_tool_proxy
from backend.app.core.mcp_tool_registry import mcp_tool_registry

router = APIRouter()
logger = logging.getLogger(__name__)


class A2ARegisterRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = ""
    endpoint: str = ""
    capabilities: list[str] = []


class A2AInvokeRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    agent_id: str = ""
    payload: dict[str, Any] = {}


class A2ARegisterResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    endpoint: str
    status: str
    capabilities: list[str]


class MCPRegisterRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = ""
    endpoint: str = ""


class MCPToolCallRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    server_id: str = ""
    tool_name: str = ""
    parameters: dict[str, Any] = {}


@router.post("/a2a/register", response_model=A2ARegisterResponse)
async def register_a2a_agent(request: A2ARegisterRequest):
    started = time.perf_counter()
    try:
        agent = a2a_registry.register(request.name, request.endpoint, request.capabilities)
        logger.info(
            "Registered A2A agent %s in %.2fms",
            request.name,
            (time.perf_counter() - started) * 1000,
        )
        return A2ARegisterResponse(**agent)
    except Exception as e:
        logger.error("Failed to register A2A agent: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/a2a")
async def list_a2a_agents():
    try:
        agents = a2a_registry.list()
        return [A2ARegisterResponse(**agent) for agent in agents]
    except Exception as e:
        logger.error("Failed to list A2A agents: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/a2a/invoke")
async def invoke_a2a_agent(request: A2AInvokeRequest):
    agent = a2a_registry.get(request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="A2A agent not found")
    try:
        result = await a2a_invoker.invoke(agent["endpoint"], request.payload)
        return result
    except Exception as e:
        logger.error("Failed to invoke A2A agent: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/mcp/servers")
async def register_mcp_server(request: MCPRegisterRequest):
    started = time.perf_counter()
    try:
        server = mcp_tool_registry.register_server(request.name, request.endpoint)
        logger.info(
            "Registered MCP server %s in %.2fms",
            request.name,
            (time.perf_counter() - started) * 1000,
        )
        return server
    except Exception as e:
        logger.error("Failed to register MCP server: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/mcp/servers/{server_id}/connect")
async def connect_mcp_server(server_id: str):
    try:
        server = mcp_tool_registry.connect(server_id)
        return server
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        logger.error("Failed to connect MCP server: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/mcp/servers/{server_id}/disconnect")
async def disconnect_mcp_server(server_id: str):
    try:
        server = mcp_tool_registry.disconnect(server_id)
        return server
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        logger.error("Failed to disconnect MCP server: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/mcp/servers")
async def list_mcp_servers():
    try:
        servers = mcp_tool_registry.list_servers()
        return servers
    except Exception as e:
        logger.error("Failed to list MCP servers: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/mcp/tools/call")
async def call_mcp_tool(request: MCPToolCallRequest):
    try:
        result = await mcp_tool_proxy.call_tool(
            request.server_id,
            request.tool_name,
            request.parameters,
        )
        return result
    except Exception as e:
        logger.error("Failed to call MCP tool: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
