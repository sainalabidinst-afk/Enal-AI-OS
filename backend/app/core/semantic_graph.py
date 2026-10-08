import json  # noqa: I001
import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum, Enum  # noqa: F401
from pathlib import Path
from typing import Any, TypedDict

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


class NodeType(StrEnum):
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


class RelationType(StrEnum):
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
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


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
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logger.warning("SemanticProjectGraph directory %s is not writable; running in read-only mode", self.base_path)
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Load persisted nodes and edges from filesystem into in-memory index."""
        for path in self.base_path.glob("node-*.json"):
            try:
                data = json.loads(path.read_text())
                node_type_str = data.get("type", "component")
                try:
                    nt = NodeType(node_type_str)
                except ValueError:
                    nt = NodeType.COMPONENT
                created_raw = data.get("created_at", datetime.now(UTC).isoformat())
                try:
                    created = datetime.fromisoformat(created_raw)
                except ValueError:
                    created = datetime.now(UTC)
                node = GraphNode(
                    id=data["id"],
                    node_type=nt,
                    name=data.get("name", ""),
                    description=data.get("description", ""),
                    properties=data.get("properties", {}),
                    project_id=data.get("project_id"),
                    created_at=created,
                )
                self._nodes[node.id] = node
            except (json.JSONDecodeError, KeyError):
                logger.warning(f"Failed to load graph node from {path}")
        for path in self.base_path.glob("edge-*.json"):
            try:
                data = json.loads(path.read_text())
                relation_str = data.get("relation", "uses")
                try:
                    rel = RelationType(relation_str)
                except ValueError:
                    rel = RelationType.USES
                edge = GraphEdge(
                    id=data["id"],
                    source_id=data["source"],
                    target_id=data["target"],
                    relation=rel,
                    properties=data.get("properties", {}),
                )
                self._edges[edge.id] = edge
            except (json.JSONDecodeError, KeyError):
                logger.warning(f"Failed to load graph edge from {path}")

    async def add_node(self, node: GraphNode) -> str:
        self._nodes[node.id] = node
        self._persist_node(node)
        return node.id

    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: RelationType,
        properties: dict[str, Any] | None = None,
    ) -> str:  # noqa: E501
        edge_id = f"edge-{uuid.uuid4().hex[:8]}"
        edge = GraphEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            properties=properties or {},
        )  # noqa: E501
        self._edges[edge_id] = edge
        self._persist_edge(edge)
        return edge_id

    async def get_related(
        self, node_id: str, relation: RelationType | None = None
    ) -> list[dict[str, Any]]:  # noqa: E501
        related: list[dict[str, Any]] = []
        for edge in self._edges.values():
            if edge.source_id == node_id or edge.target_id == node_id:
                if relation is None or edge.relation == relation:
                    related.append(
                        {
                            "edge": edge.id,
                            "relation": edge.relation.value,
                            "source": edge.source_id,
                            "target": edge.target_id,
                        }
                    )
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

    def _calculate_evidence_score(self, node: GraphNode) -> float:
        """Calculate evidence score based on sources and confidence."""
        sources = node.properties.get("sources", [])
        confidence_sum = sum(s.get("confidence", 0.5) for s in sources)
        count = len(sources)
        return round(confidence_sum / count, 2) if count > 0 else 0.5

    def _format_citation(self, node: GraphNode) -> str:
        """Format citation string for a node's sources."""
        sources = node.properties.get("sources", [])
        citations = []
        for s in sources:
            if s.get("url"):
                citations.append(f"Retrieved from {s['url']}")
            elif s.get("document"):
                citations.append(f"Source: {s['document']}")
        return "; ".join(citations) if citations else f"Internal knowledge: {node.name}"

    async def query(
        self, query_str: str, node_type: NodeType | None = None
    ) -> list[dict[str, Any]]:  # noqa: E501
        """Query nodes by name/description."""
        results = []
        query_lower = query_str.lower()
        for node in self._nodes.values():
            if node_type and node.node_type != node_type:
                continue
            if query_lower in node.name.lower() or query_lower in node.description.lower():
                results.append(
                    {
                        "id": node.id,
                        "type": node.node_type.value,
                        "name": node.name,
                        "description": node.description,
                        "evidence_score": self._calculate_evidence_score(node),
                        "citation": self._format_citation(node),
                    }
                )
        return results

    async def get_evidence(self, node_id: str) -> dict[str, Any] | None:
        """Get evidence details for a node."""
        node = self._nodes.get(node_id)
        if not node:
            return None
        return {
            "node_id": node.id,
            "evidence_score": self._calculate_evidence_score(node),
            "sources": node.properties.get("sources", []),
            "citations": self._format_citation(node),
        }


semantic_graph = SemanticProjectGraph()
