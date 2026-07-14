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
        return observability.get_trace(trace_id)

    async def get_metrics(self, agent: str | None = None) -> dict[str, Any]:
        return observability.get_metrics(agent=agent)

    async def get_artifacts(self, workspace_id: str) -> list[dict[str, Any]]:
        return await artifact_service.list_artifacts(workspace_id=workspace_id)

    async def get_graph(self, project_id: str | None = None) -> dict[str, Any]:
        nodes = []
        edges = []
        for node in semantic_graph._nodes.values():
            if project_id is None or node.project_id == project_id:
                nodes.append({"id": node.id, "type": node.node_type.value, "name": node.name})
        for edge in semantic_graph._edges.values():
            edges.append({"id": edge.id, "source": edge.source_id, "target": edge.target_id, "relation": edge.relation.value})
        return {"nodes": nodes, "edges": edges}

    async def get_memory(self, layer: str, query: str, limit: int = 10) -> list[dict]:
        return await memory_manager.search(layer, query, limit=limit)

    async def get_reputation(self) -> list[dict[str, Any]]:
        return agent_reputation.get_leaderboard(limit=50)

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
        return meta_cognition.get_metrics()

    async def export_project(self, workspace_id: str) -> dict[str, Any]:
        artifacts = await artifact_service.list_artifacts(workspace_id=workspace_id)
        graph = await self.get_graph(workspace_id)
        return {"workspace_id": workspace_id, "artifacts": [a.model_dump() for a in artifacts], "graph": graph}


ai_studio = AIStudio()
