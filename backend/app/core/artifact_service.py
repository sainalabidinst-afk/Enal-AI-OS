import asyncio
from datetime import UTC, datetime
from typing import Any

from backend.app.models.schemas_execution import Artifact, ArtifactVersion


class ArtifactService:
    def __init__(self) -> None:
        self._artifacts: dict[str, Artifact] = {}
        self._workspaces: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def create_workspace(self, name: str, description: str = "") -> Any:
        from backend.app.models.schemas_execution import Workspace
        ws = Workspace(name=name, description=description)
        async with self._lock:
            self._workspaces[ws.id] = ws
        return ws

    async def clear_workspace(self, workspace_id: str) -> bool:
        async with self._lock:
            if workspace_id in self._workspaces:
                ws = self._workspaces[workspace_id]
                if hasattr(ws, 'artifact_ids'):
                    ws.artifact_ids = []
                if hasattr(ws, 'execution_ids'):
                    ws.execution_ids = []
                to_delete = [
                    aid
                    for aid in self._artifacts
                    if self._artifacts[aid].workspace_id == workspace_id
                ]
                for aid in to_delete:
                    del self._artifacts[aid]
                return True
            return False

    async def delete_workspace(self, workspace_id: str) -> bool:
        async with self._lock:
            if workspace_id in self._workspaces:
                to_delete = [
                    aid
                    for aid in self._artifacts
                    if self._artifacts[aid].workspace_id == workspace_id
                ]
                for aid in to_delete:
                    del self._artifacts[aid]
                del self._workspaces[workspace_id]
                return True
            return False

    async def get_workspace(self, workspace_id: str) -> Any | None:
        return self._workspaces.get(workspace_id)

    async def create_artifact(
        self,
        workspace_id: str,
        name: str,
        artifact_type: str,
        description: str | None = None,
        content: str | None = None,
        path: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Artifact:
        async with self._lock:
            artifact = Artifact(
                workspace_id=workspace_id,
                name=name,
                type=artifact_type,
                description=description,
            )
            version = ArtifactVersion(
                version=1,
                created_at=datetime.now(UTC),
                content=content,
                path=path,
                metadata=metadata or {},
            )
            artifact.versions.append(version)
            self._artifacts[artifact.id] = artifact
            return artifact

    async def get_artifact(self, artifact_id: str) -> Artifact | None:
        return self._artifacts.get(artifact_id)

    async def list_artifacts(
        self, workspace_id: str | None = None, artifact_type: str | None = None
    ) -> list[Artifact]:
        artifacts = list(self._artifacts.values())
        if workspace_id:
            artifacts = [a for a in artifacts if a.workspace_id == workspace_id]
        if artifact_type:
            artifacts = [a for a in artifacts if a.type == artifact_type]
        return artifacts

    async def add_version(
        self,
        artifact_id: str,
        content: str | None = None,
        path: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Artifact | None:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        artifact.current_version += 1
        version = ArtifactVersion(
            version=artifact.current_version,
            created_at=datetime.now(UTC),
            content=content,
            path=path,
            metadata=metadata or {},
        )
        artifact.versions.append(version)
        artifact.updated_at = datetime.now(UTC)
        return artifact

    async def get_version(self, artifact_id: str, version: int) -> ArtifactVersion | None:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        for v in artifact.versions:
            if v.version == version:
                return v
        return None

    async def restore_version(self, artifact_id: str, version: int) -> Artifact | None:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        target = next((v for v in artifact.versions if v.version == version), None)
        if not target:
            return None
        artifact.current_version += 1
        restored = ArtifactVersion(
            version=artifact.current_version,
            created_at=datetime.now(UTC),
            content=target.content,
            path=target.path,
            metadata={**target.metadata, "restored_from": version},
        )
        artifact.versions.append(restored)
        artifact.updated_at = datetime.now(UTC)
        return artifact

    async def delete_artifact(self, artifact_id: str) -> bool:
        if artifact_id in self._artifacts:
            del self._artifacts[artifact_id]
            return True
        return False


artifact_service = ArtifactService()
