"""AI Studio - observability, debug, and management interface."""
import logging
from typing import Any

from backend.app.core.observability import observability
from backend.app.core.artifact_service import artifact_service
from backend.app.core.semantic_graph import semantic_graph
from backend.app.core.memory_layer import memory_manager
from backend.app.core.agent_reputation import agent_reputation
from backend.app.core.cognitive_kernel import cognitive_kernel
from backend.app.core.adaptive_runtime import adaptive_runtime
from backend.app.core.meta_cognition import meta_cognition

logger = logging.getLogger(__name__)


class AIStudio:
    async def get_trace(self, trace_id: str) -> dict[str, Any]:
        result: dict | list | None = observability.get_trace(trace_id)
        if isinstance(result, list):
            return {"traces": result, "count": len(result)}
        return result if result else {}

    async def get_metrics(self, agent: str | None = None) -> dict[str, Any]:
        result = observability.get_metrics(agent=agent)
        return result if result else {}

    async def get_artifacts(self, workspace_id: str) -> list[dict[str, Any]]:
        artifacts = await artifact_service.list_artifacts(workspace_id=workspace_id)
        return [{"id": a.id, "name": a.name, "type": a.type} for a in artifacts]

    async def get_graph(self, project_id: str | None = None) -> dict[str, Any]:
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        for node in semantic_graph._nodes.values():
            if project_id is None or node.project_id == project_id:
                nodes.append({"id": node.id, "type": node.node_type.value, "name": node.name})
        for edge in semantic_graph._edges.values():
            edges.append({"id": edge.id, "source": edge.source_id, "target": edge.target_id, "relation": edge.relation.value})
        return {"nodes": nodes, "edges": edges}

    async def get_memory(self, layer: str, query: str, limit: int = 10) -> list[dict[str, Any]]:
        result = await memory_manager.search(layer, query, limit=limit)
        return list(result)

    async def get_reputation(self) -> list[dict[str, Any]]:
        result = agent_reputation.get_leaderboard(limit=50)
        return list(result) if result else []

    async def get_cognitive_services(self) -> list[str]:
        return cognitive_kernel.list_services()

    async def get_pipeline_presets(self) -> dict[str, Any]:
        from backend.app.core.cognitive_budget import TaskComplexity
        return {
            "presets": [
                {"complexity": c.value, "pipeline": adaptive_runtime.get_pipeline_for_complexity(c), "description": adaptive_runtime.describe_pipeline(c)}
                for c in TaskComplexity
            ]
        }

    async def get_meta_metrics(self) -> dict[str, Any]:
        result = meta_cognition.get_metrics()
        return result if result else {}

    async def export_project(self, workspace_id: str) -> dict[str, Any]:
        artifacts = await artifact_service.list_artifacts(workspace_id=workspace_id)
        graph = await self.get_graph(workspace_id)
        artifact_dicts: list[dict[str, Any]] = []
        for a in artifacts:
            if hasattr(a, 'model_dump'):
                artifact_dicts.append(a.model_dump())
            elif hasattr(a, '__dict__'):
                artifact_dicts.append(a.__dict__)
            else:
                artifact_dicts.append({"id": a.id, "name": a.name, "type": a.type})
        return {"workspace_id": workspace_id, "artifacts": artifact_dicts, "graph": graph}

    async def create_workspace(self, name: str, description: str = "") -> dict[str, Any]:
        workspace = await artifact_service.create_workspace(name=name, description=description)
        if hasattr(workspace, 'created_at'):
            created = workspace.created_at.isoformat() if hasattr(workspace.created_at, 'isoformat') else str(workspace.created_at)
        else:
            created = ""
        return {"id": workspace.id, "name": workspace.name, "created_at": created}

    async def create_artifact(self, workspace_id: str, name: str, content: str, artifact_type: str = "text") -> dict[str, Any]:
        artifact = await artifact_service.create_artifact(workspace_id=workspace_id, name=name, content=content, artifact_type=artifact_type)
        return {"id": artifact.id, "name": artifact.name, "type": artifact.type}

    async def execute_task(self, task: str, workspace_id: str | None = None) -> dict[str, Any]:
        project_id = workspace_id or f"studio-task-{hash(task)}"
        result = await adaptive_runtime.execute(task, project_id=project_id)
        return {"task": task, "result": result, "project_id": project_id}

    async def clear_workspace(self, workspace_id: str) -> bool:
        try:
            return await artifact_service.clear_workspace(workspace_id)
        except Exception:
            return False

    async def delete_workspace(self, workspace_id: str) -> bool:
        try:
            return await artifact_service.delete_workspace(workspace_id)
        except Exception:
            return False


ai_studio = AIStudio()
