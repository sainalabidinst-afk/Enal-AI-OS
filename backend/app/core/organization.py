import logging
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class RoleType(str, Enum):
    CEO = "ceo"
    CTO = "cto"
    MANAGER = "manager"
    LEAD = "lead"
    SPECIALIST = "specialist"
    WORKER = "worker"


@dataclass
class OrgNode:
    id: str
    name: str
    role: RoleType
    agent_type: str
    parent_id: str | None = None
    children: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class OrganizationTree:
    def __init__(self):
        self._nodes: dict[str, OrgNode] = {}
        self._root: str | None = None

    def add_node(self, node: OrgNode) -> str:
        self._nodes[node.id] = node
        if node.parent_id and node.parent_id in self._nodes:
            self._nodes[node.parent_id].children.append(node.id)
        if not self._root:
            self._root = node.id
        return node.id

    def get(self, node_id: str) -> OrgNode | None:
        return self._nodes.get(node_id)

    def get_children(self, node_id: str) -> list[OrgNode]:
        node = self._nodes.get(node_id)
        if not node:
            return []
        return [self._nodes[c] for c in node.children if c in self._nodes]

    def get_path(self, node_id: str) -> list[OrgNode]:
        path: list[OrgNode] = []
        current = self._nodes.get(node_id)
        while current:
            path.insert(0, current)
            current = self._nodes.get(current.parent_id) if current.parent_id else None
        return path

    def find_by_capability(self, capability: str) -> list[OrgNode]:
        return [n for n in self._nodes.values() if capability in n.capabilities]

    def get_subtree(self, node_id: str) -> dict[str, Any]:
        node = self._nodes.get(node_id)
        if not node:
            return {}
        return {
            "id": node.id,
            "name": node.name,
            "role": node.role.value,
            "agent_type": node.agent_type,
            "children": [self.get_subtree(c) for c in node.children],
        }


organization_tree = OrganizationTree()
