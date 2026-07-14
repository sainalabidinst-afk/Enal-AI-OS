from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio

from backend.app.models.schemas_execution import Artifact, ArtifactVersion


class ArtifactService:
    def __init__(self) -> None:
        self._artifacts: Dict[str, Artifact] = {}
        self._lock = asyncio.Lock()

    async def create_artifact(self, workspace_id: str, name: str, artifact_type: str, description: Optional[str] = None, content: Optional[str] = None, path: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Artifact:
        async with self._lock:
            artifact = Artifact(workspace_id=workspace_id, name=name, type=artifact_type, description=description)
            version = ArtifactVersion(version=1, content=content, path=path, metadata=metadata or {})
            artifact.versions.append(version)
            self._artifacts[artifact.id] = artifact
            return artifact

    async def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        return self._artifacts.get(artifact_id)

    async def list_artifacts(self, workspace_id: Optional[str] = None, artifact_type: Optional[str] = None) -> List[Artifact]:
        artifacts = list(self._artifacts.values())
        if workspace_id:
            artifacts = [a for a in artifacts if a.workspace_id == workspace_id]
        if artifact_type:
            artifacts = [a for a in artifacts if a.type == artifact_type]
        return artifacts

    async def add_version(self, artifact_id: str, content: Optional[str] = None, path: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Optional[Artifact]:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        artifact.current_version += 1
        version = ArtifactVersion(version=artifact.current_version, content=content, path=path, metadata=metadata or {})
        artifact.versions.append(version)
        artifact.updated_at = datetime.utcnow()
        return artifact

    async def get_version(self, artifact_id: str, version: int) -> Optional[ArtifactVersion]:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        for v in artifact.versions:
            if v.version == version:
                return v
        return None

    async def restore_version(self, artifact_id: str, version: int) -> Optional[Artifact]:
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        target = next((v for v in artifact.versions if v.version == version), None)
        if not target:
            return None
        artifact.current_version += 1
        restored = ArtifactVersion(version=artifact.current_version, content=target.content, path=target.path, metadata={**target.metadata, "restored_from": version})
        artifact.versions.append(restored)
        artifact.updated_at = datetime.utcnow()
        return artifact

    async def delete_artifact(self, artifact_id: str) -> bool:
        if artifact_id in self._artifacts:
            del self._artifacts[artifact_id]
            return True
        return False


artifact_service = ArtifactService()
