import logging
import json
import uuid
from pathlib import Path
from typing import Any, TypedDict
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


def _empty_properties() -> dict[str, Any]:
    return {}


class GraphNodeData(TypedDict):
    id: str
    type: str
    name: str
    description: str
    properties: dict[str, Any]
    project_id: str | None
    created_at: str


class GraphEdgeData(TypedDict):
    id: str
    source: str
    target: str
    relation: str
    properties: dict[str, Any]


class NodeType(str, Enum):
    PROJECT = "project"
    REQUIREMENT = "requirement"
    COMPONENT = "component"
    API = "api"
    DATABASE = "database"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    TEST = "test"
    DOCUMENT = "document"


class RelationType(str, Enum):
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    USES = "uses"
    CONNECTS_TO = "connects_to"
    PART_OF = "part_of"
    TRIGGERS = "triggers"
    MONITORS = "monitors"


@dataclass
class GraphNode:
    id: str
    node_type: NodeType
    name: str
    description: str
    properties: dict[str, Any] = field(default_factory=_empty_properties)
    project_id: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class GraphEdge:
    id: str
    source_id: str
    target_id: str
    relation: RelationType
    properties: dict[str, Any] = field(default_factory=_empty_properties)


class SemanticProjectGraph:
    def __init__(self, base_path: str = "./workspace/graph"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}

    async def add_node(self, node: GraphNode) -> str:
        self._nodes[node.id] = node
        self._persist_node(node)
        return node.id

    async def add_edge(self, source_id: str, target_id: str, relation: RelationType, properties: dict[str, Any] | None = None) -> str:
        edge_id = f"edge-{uuid.uuid4().hex[:8]}"
        edge = GraphEdge(id=edge_id, source_id=source_id, target_id=target_id, relation=relation, properties=properties or {})
        self._edges[edge_id] = edge
        self._persist_edge(edge)
        return edge_id

    async def get_related(self, node_id: str, relation: RelationType | None = None) -> list[dict[str, Any]]:
        related: list[dict[str, Any]] = []
        for edge in self._edges.values():
            if edge.source_id == node_id or edge.target_id == node_id:
                if relation is None or edge.relation == relation:
                    related.append({
                        "edge": edge.id,
                        "relation": edge.relation.value,
                        "source": edge.source_id,
                        "target": edge.target_id,
                    })
        return related

    async def get_dependencies(self, node_id: str) -> list[GraphNode]:
        deps: list[GraphNode] = []
        for edge in self._edges.values():
            if edge.target_id == node_id and edge.relation == RelationType.DEPENDS_ON:
                dep_node = self._nodes.get(edge.source_id)
                if dep_node:
                    deps.append(dep_node)
        return deps

    async def get_dependents(self, node_id: str) -> list[GraphNode]:
        dependents: list[GraphNode] = []
        for edge in self._edges.values():
            if edge.source_id == node_id and edge.relation == RelationType.DEPENDS_ON:
                dep_node = self._nodes.get(edge.target_id)
                if dep_node:
                    dependents.append(dep_node)
        return dependents

    async def propagate_change(self, node_id: str, change: dict[str, Any]) -> list[str]:
        _ = change
        affected: list[str] = []
        queue: list[str] = [node_id]
        visited: set[str] = set()
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            dependents = await self.get_dependents(current)
            for dep in dependents:
                affected.append(dep.id)
                queue.append(dep.id)
        return affected

    def _persist_node(self, node: GraphNode):
        path = self.base_path / f"node-{node.id}.json"
        data: GraphNodeData = {
            "id": node.id,
            "type": node.node_type.value,
            "name": node.name,
            "description": node.description,
            "properties": node.properties,
            "project_id": node.project_id,
            "created_at": node.created_at.isoformat(),
        }
        path.write_text(json.dumps(data, indent=2))

    def _persist_edge(self, edge: GraphEdge):
        path = self.base_path / f"edge-{edge.id}.json"
        data: GraphEdgeData = {
            "id": edge.id,
            "source": edge.source_id,
            "target": edge.target_id,
            "relation": edge.relation.value,
            "properties": edge.properties,
        }
        path.write_text(json.dumps(data, indent=2))


semantic_graph = SemanticProjectGraph()
