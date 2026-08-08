from fastapi import APIRouter, HTTPException, Query

from backend.app.core.artifact_service import artifact_service
from backend.app.models.schemas_execution import Artifact, ArtifactVersion

router = APIRouter()


@router.post("/artifacts", response_model=Artifact)
async def create_artifact(
    workspace_id: str,
    name: str,
    artifact_type: str,
    description: str | None = None,
    content: str | None = None,
    path: str | None = None,
    metadata: dict | None = None,
):
    artifact = await artifact_service.create_artifact(
        workspace_id=workspace_id,
        name=name,
        artifact_type=artifact_type,
        description=description,
        content=content,
        path=path,
        metadata=metadata,
    )
    return artifact


@router.get("/artifacts", response_model=list[Artifact])
async def list_artifacts(
    workspace_id: str | None = Query(None),
    artifact_type: str | None = Query(None),
):
    return await artifact_service.list_artifacts(
        workspace_id=workspace_id, artifact_type=artifact_type
    )


@router.get("/artifacts/{artifact_id}", response_model=Artifact)
async def get_artifact(artifact_id: str):
    artifact = await artifact_service.get_artifact(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@router.get("/artifacts/{artifact_id}/versions/{version}", response_model=ArtifactVersion)
async def get_artifact_version(artifact_id: str, version: int):
    v = await artifact_service.get_version(artifact_id, version)
    if not v:
        raise HTTPException(status_code=404, detail="Artifact version not found")
    return v


@router.post("/artifacts/{artifact_id}/versions", response_model=Artifact)
async def add_artifact_version(
    artifact_id: str,
    content: str | None = None,
    path: str | None = None,
    metadata: dict | None = None,
):
    artifact = await artifact_service.add_version(
        artifact_id, content=content, path=path, metadata=metadata
    )
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@router.post("/artifacts/{artifact_id}/restore/{version}", response_model=Artifact)
async def restore_artifact_version(artifact_id: str, version: int):
    artifact = await artifact_service.restore_version(artifact_id, version)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@router.delete("/artifacts/{artifact_id}")
async def delete_artifact(artifact_id: str):
    deleted = await artifact_service.delete_artifact(artifact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return {"deleted": True}
