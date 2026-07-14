from fastapi import APIRouter, HTTPException, Query
from backend.app.models.schemas_execution import (
    ExecutionSession,
    ExecutionStatus,
    ExecutionPhase,
    ExecutionArtifact,
)
from backend.app.core.execution_session import execution_session_manager
from backend.app.core.execution_integration import execution_integration
from backend.app.core.workspace_service import workspace_service
from backend.app.core.artifact_service import artifact_service

router = APIRouter()


@router.post("/executions", response_model=ExecutionSession)
async def create_execution(goal: str, conversation_id: str | None = None, workspace_id: str | None = None):
    session = await execution_session_manager.create_session(
        goal=goal,
        conversation_id=conversation_id,
        workspace_id=workspace_id,
    )
    await execution_session_manager.add_log(session.id, "Execution session created", level="info")
    return session


@router.get("/executions/{execution_id}", response_model=ExecutionSession)
async def get_execution(execution_id: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    return session


@router.get("/executions", response_model=list[ExecutionSession])
async def list_executions(workspace_id: str | None = Query(None)):
    return await execution_session_manager.list_sessions(workspace_id=workspace_id)


@router.post("/executions/{execution_id}/phases", response_model=ExecutionPhase)
async def add_phase(execution_id: str, name: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    phase = await execution_session_manager.add_phase(execution_id, name)
    await execution_session_manager.add_log(execution_id, f"Phase added: {name}", metadata={"phase_id": phase.id})
    return phase


@router.patch("/executions/{execution_id}/phases/{phase_id}", response_model=ExecutionPhase)
async def update_phase(execution_id: str, phase_id: str, status: ExecutionStatus, progress: float | None = None):
    phase = await execution_session_manager.update_phase(execution_id, phase_id, status, progress)
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    return phase


@router.post("/executions/{execution_id}/progress")
async def update_progress(execution_id: str, progress: float, eta_seconds: int | None = None):
    session = await execution_session_manager.update_progress(execution_id, progress, eta_seconds)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"progress": session.progress, "eta_seconds": session.eta_seconds}


@router.post("/executions/{execution_id}/logs")
async def add_log(execution_id: str, message: str, level: str = "info", metadata: dict | None = None):
    entry = await execution_session_manager.add_log(execution_id, message, level, metadata)
    if not entry:
        raise HTTPException(status_code=404, detail="Execution not found")
    return entry


@router.get("/executions/{execution_id}/logs")
async def get_logs(execution_id: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"execution_id": execution_id, "logs": session.logs}


@router.post("/executions/{execution_id}/artifacts", response_model=ExecutionArtifact)
async def add_artifact(execution_id: str, name: str, artifact_type: str, content: str | None = None, path: str | None = None, metadata: dict | None = None):
    artifact = await execution_session_manager.add_artifact(execution_id, name, artifact_type, content, path, metadata)
    if not artifact:
        raise HTTPException(status_code=404, detail="Execution not found")
    await execution_session_manager.add_log(execution_id, f"Artifact added: {name}", metadata={"artifact_id": artifact.id})
    return artifact


@router.get("/executions/{execution_id}/artifacts", response_model=list[ExecutionArtifact])
async def list_artifacts(execution_id: str):
    session = await execution_session_manager.get_session(execution_id)
    if not session:
        raise HTTPException(status_code=404, detail="Execution not found")
    artifacts = []
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
    ws = await workspace_service.get_workspace(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    session = await execution_integration.execute(goal=goal, workspace_id=workspace_id, conversation_id=conversation_id)
    artifacts = []
    for artifact_id in session.artifacts:
        art = await artifact_service.get_artifact(artifact_id)
        if art:
            artifacts.append(art)
    return {
        "execution": session,
        "artifacts": artifacts,
    }
