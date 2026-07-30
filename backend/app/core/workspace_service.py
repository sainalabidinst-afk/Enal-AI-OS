import asyncio
from datetime import datetime, timezone
from typing import Any

from backend.app.models.schemas_execution import Workspace


class WorkspaceService:
    def __init__(self) -> None:
        self._workspaces: dict[str, Workspace] = {}
        self._lock = asyncio.Lock()

    async def create_workspace(self, name: str, description: str | None = None) -> Workspace:
        async with self._lock:
            ws = Workspace(name=name, description=description)
            self._workspaces[ws.id] = ws
            return ws

    async def get_workspace(self, workspace_id: str) -> Workspace | None:
        return self._workspaces.get(workspace_id)

    async def list_workspaces(self) -> list[Workspace]:
        return list(self._workspaces.values())

    async def add_file(self, workspace_id: str, filename: str, path: str, size: int, metadata: dict[str, Any] | None = None) -> Workspace | None:
        ws = self._workspaces.get(workspace_id)
        if not ws:
            return None
        ws.files.append({"filename": filename, "path": path, "size": size, "uploaded_at": datetime.now(timezone.utc).isoformat(), "metadata": metadata or {}})
        ws.updated_at = datetime.now(timezone.utc)
        return ws

    async def list_files(self, workspace_id: str) -> list[dict[str, Any]] | None:
        ws = self._workspaces.get(workspace_id)
        if not ws:
            return None
        return ws.files

    async def get_file(self, workspace_id: str, filename: str) -> dict[str, Any] | None:
        ws = self._workspaces.get(workspace_id)
        if not ws:
            return None
        for f in ws.files:
            if f.get("filename") == filename:
                return f
        return None

    async def delete_file(self, workspace_id: str, filename: str) -> bool:
        ws = self._workspaces.get(workspace_id)
        if not ws:
            return False
        before = len(ws.files)
        ws.files = [f for f in ws.files if f.get("filename") != filename]
        if len(ws.files) != before:
            ws.updated_at = datetime.now(timezone.utc)
            return True
        return False

    async def add_memory(self, workspace_id: str, key: str, value: Any) -> Workspace | None:
        ws = self._workspaces.get(workspace_id)
        if not ws:
            return None
        ws.memory[key] = value
        ws.updated_at = datetime.now(timezone.utc)
        return ws

    async def get_memory(self, workspace_id: str, key: str) -> Any:
        ws = self._workspaces.get(workspace_id)
        if not ws:
            return None
        return ws.memory.get(key)

    async def delete_workspace(self, workspace_id: str) -> bool:
        if workspace_id in self._workspaces:
            del self._workspaces[workspace_id]
            return True
        return False


workspace_service = WorkspaceService()

