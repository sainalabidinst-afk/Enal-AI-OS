from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.auth import require_permission
from backend.app.core.workspace_service import workspace_service
from backend.app.models.schemas_execution import Workspace

router = APIRouter()


@router.post("/workspaces", response_model=Workspace, dependencies=[Depends(require_permission("write"))])
async def create_workspace(name: str, description: str | None = None):
    ws = await workspace_service.create_workspace(name=name, description=description)
    return ws


@router.get("/workspaces", response_model=list[Workspace], dependencies=[Depends(require_permission("read"))])
async def list_workspaces():
    return await workspace_service.list_workspaces()


@router.get("/workspaces/{workspace_id}", response_model=Workspace, dependencies=[Depends(require_permission("read"))])
async def get_workspace(workspace_id: str):
    ws = await workspace_service.get_workspace(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws


@router.post("/workspaces/{workspace_id}/files", dependencies=[Depends(require_permission("write"))])
async def add_file(workspace_id: str, filename: str, path: str, size: int, metadata: dict | None = None):
    ws = await workspace_service.add_file(workspace_id, filename=filename, path=path, size=size, metadata=metadata)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"workspace_id": workspace_id, "filename": filename, "path": path}


@router.get("/workspaces/{workspace_id}/files", dependencies=[Depends(require_permission("read"))])
async def list_files(workspace_id: str):
    files = await workspace_service.list_files(workspace_id)
    if files is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"workspace_id": workspace_id, "files": files}


@router.get("/workspaces/{workspace_id}/files/{filename}", dependencies=[Depends(require_permission("read"))])
async def get_file(workspace_id: str, filename: str):
    f = await workspace_service.get_file(workspace_id, filename)
    if f is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"workspace_id": workspace_id, "filename": filename, "path": f.get("path"), "size": f.get("size"), "uploaded_at": f.get("uploaded_at"), "metadata": f.get("metadata")}


@router.delete("/workspaces/{workspace_id}/files/{filename}", dependencies=[Depends(require_permission("write"))])
async def delete_file(workspace_id: str, filename: str):
    ok = await workspace_service.delete_file(workspace_id, filename)
    if not ok:
        raise HTTPException(status_code=404, detail="Workspace or file not found")
    return {"workspace_id": workspace_id, "filename": filename, "deleted": True}


@router.post("/workspaces/{workspace_id}/memory", dependencies=[Depends(require_permission("write"))])
async def set_memory(workspace_id: str, key: str, value: Any):
    ws = await workspace_service.add_memory(workspace_id, key, value)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"workspace_id": workspace_id, "key": key}


@router.get("/workspaces/{workspace_id}/memory/{key}", dependencies=[Depends(require_permission("read"))])
async def get_memory(workspace_id: str, key: str):
    value = await workspace_service.get_memory(workspace_id, key)
    if value is None and await workspace_service.get_workspace(workspace_id) is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"workspace_id": workspace_id, "key": key, "value": value}


@router.delete("/workspaces/{workspace_id}", dependencies=[Depends(require_permission("write"))])
async def delete_workspace(workspace_id: str):
    deleted = await workspace_service.delete_workspace(workspace_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"deleted": True}
