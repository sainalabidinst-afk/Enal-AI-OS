import logging
import uuid
from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from backend.app.core.event_bus import Event, event_bus
from backend.app.core.task_queue import Task

logger = logging.getLogger(__name__)


class NodeStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"


class NodeCapability(str, Enum):
    REASONING = "reasoning"
    EXECUTION = "execution"
    SIMULATION = "simulation"
    LEARNING = "learning"


@dataclass
class RuntimeNode:
    id: str
    name: str
    capabilities: list[NodeCapability]
    status: NodeStatus = NodeStatus.ONLINE
    load: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class DistributedRuntime:
    def __init__(self):
        self._nodes: dict[str, RuntimeNode] = {}
        self._local_node_id = f"node-{uuid.uuid4().hex[:8]}"

    async def register_node(self, name: str, capabilities: list[NodeCapability]) -> str:
        node_id = f"node-{uuid.uuid4().hex[:8]}"
        node = RuntimeNode(id=node_id, name=name, capabilities=capabilities)
        self._nodes[node_id] = node
        await event_bus.publish(Event(event_type="node.registered", payload={"node_id": node_id, "name": name}, source="distributed-runtime"))
        return node_id

    async def get_node(self, node_id: str) -> RuntimeNode | None:
        return self._nodes.get(node_id)

    async def find_capable_nodes(self, capability: NodeCapability) -> list[RuntimeNode]:
        return [n for n in self._nodes.values() if capability in n.capabilities and n.status == NodeStatus.ONLINE]

    async def get_cluster_status(self) -> dict[str, Any]:
        return {
            "total_nodes": len(self._nodes),
            "online_nodes": sum(1 for n in self._nodes.values() if n.status == NodeStatus.ONLINE),
            "nodes": [{"id": n.id, "name": n.name, "capabilities": [c.value for c in n.capabilities], "status": n.status.value} for n in self._nodes.values()],
        }

    async def execute_distributed(self, task: Task, capability: NodeCapability) -> dict[str, Any]:
        nodes = await self.find_capable_nodes(capability)
        if not nodes:
            return {"error": f"No nodes available for capability: {capability}"}
        selected = min(nodes, key=lambda n: n.load)
        return {"assigned_to": selected.id, "node_name": selected.name, "task_id": task.id}


distributed_runtime = DistributedRuntime()
