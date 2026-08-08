import logging
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.auth import require_permission
from backend.app.core.workspace_service import workspace_service
from backend.app.models.schemas import ChatRequest

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/capabilities")
async def list_capabilities():
    from apps import APPS

    capabilities = []
    for app_id, app in APPS.items():
        if app is None:
            continue
        capabilities.append({
            "id": app_id,
            "name": app.name,
            "version": app.version,
            "description": app.description,
            "category": app.category,
        })
    return {"capabilities": capabilities}


@router.get("/capabilities/{capability_id}")
async def get_capability(capability_id: str):
    from apps import get_app

    app = get_app(capability_id)
    if app is None:
        raise HTTPException(status_code=404, detail=f"Capability '{capability_id}' not found")
    return app.to_dict()


@router.post(
    "/capabilities/{capability_id}/execute",
    dependencies=[Depends(require_permission("execute"))],
)
async def execute_capability(capability_id: str, request: ChatRequest):
    from apps import get_app

    app = get_app(capability_id)
    if app is None:
        raise HTTPException(status_code=404, detail=f"Capability '{capability_id}' not found")

    workspace_id = request.workspace_id or str(uuid.uuid4())
    ws = await workspace_service.get_workspace(workspace_id)
    if not ws:
        ws = await workspace_service.create_workspace(name=f"{app.name} workspace")

    started = time.perf_counter()
    status = "success"
    error = None

    try:
        result = await app.run(
            user_input=request.message,
            context={
                "workspace_id": workspace_id,
                "conversation_id": request.conversation_id,
            },
        )
        return result
    except Exception as exc:
        status = "error"
        error = str(exc)
        logger.error(f"Capability execution error for {capability_id}: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        total_ms = (time.perf_counter() - started) * 1000
        try:
            from backend.app.core.telemetry.service import record_execution_event
            record_execution_event(
                capability_id=capability_id,
                workspace_id=workspace_id,
                status=status,
                error=error,
                total_time_ms=round(total_ms, 2),
            )
        except Exception as telemetry_error:
            logger.debug(f"Capability execution telemetry recording failed: {telemetry_error}")
