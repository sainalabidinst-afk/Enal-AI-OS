"""
Knowledge Graph
================

Structured representation of network knowledge.
Connects concepts, vendors, configurations, and relationships.
"""

from dataclasses import dataclass, field
from typing import Any

from apps.network_engineer.nic.knowledge.ontology import UniversalConcept


@dataclass
class KnowledgeNode:
    id: str
    label: str
    concept: UniversalConcept | None = None
    vendor: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeEdge:
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0


class KnowledgeGraph:
    """Graph-based knowledge representation."""

    def __init__(self):
        self._nodes: dict[str, KnowledgeNode] = {}
        self._edges: list[KnowledgeEdge] = []

    def add_node(self, node: KnowledgeNode) -> None:
        self._nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        self._edges.append(edge)

    def get_related(self, node_id: str, relation: str | None = None) -> list[KnowledgeNode]:
        related_ids = set()
        for edge in self._edges:
            if edge.source_id == node_id:
                if relation is None or edge.relation == relation:
                    related_ids.add(edge.target_id)
            elif edge.target_id == node_id:
                if relation is None or edge.relation == relation:
                    related_ids.add(edge.source_id)
        return [self._nodes[nid] for nid in related_ids if nid in self._nodes]

    def find_by_concept(self, concept: UniversalConcept) -> list[KnowledgeNode]:
        return [n for n in self._nodes.values() if n.concept == concept]

    def find_by_vendor(self, vendor: str) -> list[KnowledgeNode]:
        return [n for n in self._nodes.values() if n.vendor == vendor]

    def get_all_nodes(self) -> list[KnowledgeNode]:
        return list(self._nodes.values())

    def get_all_edges(self) -> list[KnowledgeEdge]:
        return list(self._edges)


def build_default_knowledge_graph() -> KnowledgeGraph:
    """Build default knowledge graph with common network concepts."""
    graph = KnowledgeGraph()

    concepts = [
        ("concept-ha", "High Availability", UniversalConcept.HIGH_AVAILABILITY),
        ("concept-ft", "Traffic Filtering", UniversalConcept.TRAFFIC_FILTERING),
        ("concept-nat", "Address Translation", UniversalConcept.ADDRESS_TRANSLATION),
        ("concept-ip", "IP Management", UniversalConcept.IP_MANAGEMENT),
        ("concept-route", "Routing", UniversalConcept.ROUTING),
        ("concept-auth", "Authentication", UniversalConcept.AUTHENTICATION),
        ("concept-mon", "Monitoring", UniversalConcept.MONITORING),
        ("concept-backup", "Backup", UniversalConcept.BACKUP),
        ("concept-dns", "DNS Resolution", UniversalConcept.DNS_RESOLUTION),
        ("concept-ntp", "Time Synchronization", UniversalConcept.TIME_SYNCHRONIZATION),
        ("concept-vpn", "VPN", UniversalConcept.VPN),
        ("concept-qos", "QoS", UniversalConcept.QOS),
        ("concept-logging", "Logging", UniversalConcept.LOGGING),
        ("concept-vlan", "VLAN", UniversalConcept.VLAN),
    ]

    for node_id, label, concept in concepts:
        graph.add_node(KnowledgeNode(id=node_id, label=label, concept=concept))

    vendor_mappings = [
        ("vendor-cisco-hsrp", "cisco", "concept-ha", "implements"),
        ("vendor-cisco-acl", "cisco", "concept-ft", "implements"),
        ("vendor-cisco-nat", "cisco", "concept-nat", "implements"),
        ("vendor-fortinet-ha", "fortinet", "concept-ha", "implements"),
        ("vendor-fortinet-fw", "fortinet", "concept-ft", "implements"),
        ("vendor-mikrotik-vrrp", "mikrotik", "concept-ha", "implements"),
        ("vendor-mikrotik-fw", "mikrotik", "concept-ft", "implements"),
    ]

    for node_id, vendor, target_id, relation in vendor_mappings:
        graph.add_node(KnowledgeNode(id=node_id, label=node_id, vendor=vendor))
        graph.add_edge(KnowledgeEdge(source_id=node_id, target_id=target_id, relation=relation))

    return graph


knowledge_graph = build_default_knowledge_graph()
