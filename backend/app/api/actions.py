from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from backend.app.connectors.base_action import (
    ActionConnectorError,
    ActionRequest,
    ActionResult,
    ActionType,
    action_connector_manager,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("/connectors")
async def list_connectors() -> dict[str, list[dict[str, Any]]]:
    """List all registered action connectors."""
    connectors = await action_connector_manager.list_connectors()
    return {"connectors": connectors}


@router.post("/execute", response_model=ActionResult)
async def execute_action(
    request: ActionRequest = Body(
        ...,
        example={
            "action": "read_file",
            "params": {"path": "docs/README.md"},
            "connector": "file_system",
        }
    ),
) -> ActionResult:
    """Execute an action on a specified connector.

    Example::

        POST /api/v1/actions/execute
        {
            "action": "read_file",
            "params": {"path": "docs/README.md"},
            "connector": "file_system"
        }
    """
    try:
        connector = await action_connector_manager.get_connector(request.connector)
        if not connector.connected:
            await connector.connect()
        result = await connector.execute(request.action, request.params)
        return result
    except ActionConnectorError as e:
        logger.error("Action failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Unexpected error executing action: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/connect", response_model=dict[str, Any])
async def connect_connector(
    connector_name: str = Body(..., embed=True, example="file_system"),
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Connect a specific action connector with optional config."""
    try:
        connector = await action_connector_manager.get_connector(connector_name)
        if config:
            for key, value in config.items():
                if hasattr(connector, f"_{key}"):
                    setattr(connector, f"_{key}", value)
        await connector.connect()
        return {"connector": connector_name, "connected": True}
    except ActionConnectorError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/disconnect", response_model=dict[str, Any])
async def disconnect_connector(
    connector_name: str = Body(..., embed=True, example="file_system"),
) -> dict[str, Any]:
    """Disconnect a specific action connector."""
    try:
        connector = await action_connector_manager.get_connector(connector_name)
        await connector.disconnect()
        return {"connector": connector_name, "connected": False}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/connectors/{connector_name}/actions")
async def list_connector_actions(connector_name: str) -> dict[str, str | list[str]]:
    """List available actions for a specific connector."""
    try:
        connector = await action_connector_manager.get_connector(connector_name)
        actions = await connector.list_actions()
        return {"connector": connector_name, "actions": actions}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/types")
async def list_action_types() -> dict[str, list[str]]:
    """List all available action connector types."""
    return {"types": [t.value for t in ActionType]}
