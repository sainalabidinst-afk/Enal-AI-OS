import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.core.artifact_service import artifact_service
from backend.app.core.auth import require_permission
from backend.app.core.execution_integration import execution_integration
from backend.app.core.execution_session import execution_session_manager
from backend.app.core.telemetry.service import record_execution_event
from backend.app.core.workspace_service import workspace_service
from backend.app.models.schemas_execution import (
    ExecutionArtifact,
    ExecutionPhase,
    ExecutionSession,
    ExecutionStatus,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/executions",
    response_model=ExecutionSession,
    dependencies=[Depends(require_permission("execute"))],
)
async def create_execution(
    goal: str,
    conversation_id: str | None = None,
    workspace_id: str | None = None,
):
    session = await execution_session_manager.create_session(
        goal=goal,
        conversation_id=conversation_id,
        workspace_id=workspace_id,
    )
    await execution_session_manager.add_log(session.id, "Execution session created", level="info")
    return session


@router.get(
    "/executions/{execution_id}",
    response_model=ExecutionSession,
    dependencies=[Depends(require_permission("read"))],
)
async def get_execution(execution_id: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    return session


@router.get(
    "/executions",
    response_model=list[ExecutionSession],
    dependencies=[Depends(require_permission("read"))],
)
async def list_executions(workspace_id: str | None = Query(None)):
    return await execution_session_manager.list_sessions(workspace_id=workspace_id)


@router.post(
    "/executions/{execution_id}/phases",
    response_model=ExecutionPhase,
    dependencies=[Depends(require_permission("write"))],
)
async def add_phase(execution_id: str, name: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    phase_result = await execution_session_manager.add_phase(execution_id, name)
    if not phase_result:
        raise HTTPException(status_code=500, detail="Failed to create phase")
    phase_id = phase_result.get("id", "")
    await execution_session_manager.add_log(
        execution_id,
        f"Phase added: {name}",
        metadata={"phase_id": phase_id},
    )
    return phase_result


@router.patch(
    "/executions/{execution_id}/phases/{phase_id}",
    response_model=ExecutionPhase,
    dependencies=[Depends(require_permission("write"))],
)
async def update_phase(
    execution_id: str,
    phase_id: str,
    status: ExecutionStatus,
    progress: float | None = None,
):
    phase = await execution_session_manager.update_phase(execution_id, phase_id, status, progress)
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    return phase


@router.post(
    "/executions/{execution_id}/progress",
    dependencies=[Depends(require_permission("write"))],
)
async def update_progress(execution_id: str, progress: float, eta_seconds: int | None = None):
    session = await execution_session_manager.update_progress(execution_id, progress, eta_seconds)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"progress": session.progress, "eta_seconds": session.eta_seconds}


@router.post("/executions/{execution_id}/logs", dependencies=[Depends(require_permission("write"))])
async def add_log(
    execution_id: str,
    message: str,
    level: str = "info",
    metadata: dict | None = None,
):
    entry = await execution_session_manager.add_log(execution_id, message, level, metadata)
    if not entry:
        raise HTTPException(status_code=404, detail="Execution not found")
    return entry


@router.get("/executions/{execution_id}/logs", dependencies=[Depends(require_permission("read"))])
async def get_logs(execution_id: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"execution_id": execution_id, "logs": session.logs}


@router.post(
    "/executions/{execution_id}/artifacts",
    response_model=ExecutionArtifact,
    dependencies=[Depends(require_permission("write"))],
)
async def add_artifact(
    execution_id: str,
    name: str,
    artifact_type: str,
    content: str | None = None,
    path: str | None = None,
    metadata: dict | None = None,
):
    artifact = await execution_session_manager.add_artifact(
        execution_id, name, artifact_type, content, path, metadata
    )
    if not artifact:
        raise HTTPException(status_code=404, detail="Execution not found")
    await execution_session_manager.add_log(
        execution_id,
        f"Artifact added: {name}",
        metadata={"artifact_id": artifact.id},
    )
    return artifact


@router.get(
    "/executions/{execution_id}/artifacts",
    response_model=list[ExecutionArtifact],
    dependencies=[Depends(require_permission("read"))],
)
async def list_artifacts(execution_id: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    artifacts: list[ExecutionArtifact] = []
    for artifact_id in session.artifacts:
        art = await execution_session_manager.get_execution_artifact(artifact_id)
        if art:
            artifacts.append(art)
    return artifacts


@router.post("/executions/{execution_id}/cancel")
async def cancel_execution(execution_id: str):
    session = await execution_session_manager.update_status(execution_id, ExecutionStatus.cancelled)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    await execution_session_manager.add_log(execution_id, "Execution cancelled", level="warning")
    return {"status": "cancelled", "execution_id": execution_id}


@router.delete("/executions/{execution_id}")
async def delete_execution(execution_id: str):
    deleted = await execution_session_manager.delete_session(execution_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"deleted": True}


@router.post("/executions/run")
async def run_execution(goal: str, workspace_id: str, conversation_id: str | None = None):
    started = time.perf_counter()
    status = "success"
    error = None
    execution: ExecutionSession | None = None
    try:
        ws = await workspace_service.get_workspace(workspace_id)
        if not ws:
            raise HTTPException(status_code=404, detail="Workspace not found")
        execution = await execution_integration.execute(
            goal=goal,
            workspace_id=workspace_id,
            conversation_id=conversation_id,
        )
        artifacts: list[dict[str, Any]] = []
        if execution:
            for artifact_id in execution.artifacts:
                art = await artifact_service.get_artifact(artifact_id)
                if art:
                    artifacts.append({
                        "id": art.id,
                        "name": getattr(art, 'name', artifact_id),
                        "type": getattr(art, 'type', ''),
                        "execution_id": execution.id,
                        "metadata": getattr(art, 'metadata', {}),
                    })
        return {
            "execution": execution,
            "artifacts": artifacts,
        }
    except Exception as exc:
        status = "error"
        error = str(exc)
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        total_ms = (time.perf_counter() - started) * 1000
        try:
            record_execution_event(
                execution_id=execution.id if execution else "unknown",
                status=status,
                goal=goal,
                error=error,
                total_time_ms=round(total_ms, 2),
            )
        except Exception as telemetry_error:
            logger.debug("Execution telemetry recording failed: %s", telemetry_error)
