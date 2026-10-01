"""
Edge Extractor — extracts relationships between entities.

Analyzes node content, descriptions, and context to discover
relationships (correlations, dependencies, contradictions)
between entities across domains and memory layers.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.cross_domain_graph.entity_resolver import EntityResolver
from apps.cross_domain_graph.schemas import (
    GraphEdge,
    GraphNode,
    RelationType,
)

logger = logging.getLogger(__name__)


# Common relationship keywords and their relation types
_RELATION_PATTERNS: list[tuple[str, RelationType]] = [
    (r"\bdepends on\b|\breliant on\b|\brequires\b|\bneeds\b", RelationType.DEPENDS_ON),
    (r"\bcorrelat(?:s|ed|ion)\b|\bassociated with\b|\brelated to\b", RelationType.CORRELATES_WITH),
    (r"\bcontradict(?:s|ed|ion)\b|\bopposing view\b|\bdisagree\b", RelationType.CONTRADICTS),
    (r"\bcauses?\b|\btriggers?\b|\bleads to\b|\bresults in\b", RelationType.CAUSES),
    (r"\bsupersedes?\b|\boverrides\b|\breplaces\b", RelationType.SUPERSEDES),
    (r"\bpart of\b|\bcontains\b|\bincludes\b|\bwithin\b", RelationType.PART_OF),
    (r"\bsame as\b|\bequivalent to\b|\bidentical to\b", RelationType.SAME_AS),
    (r"\breferences?\b|\bcites?\b|\bbased on\b", RelationType.REFERENCES),
]


class EdgeExtractor:
    """
    Extracts relationship edges between graph nodes.

    Usage::

        extractor = EdgeExtractor()
        edges = extractor.extract_edges(nodes, context)
    """

    def __init__(self, resolver: EntityResolver | None = None) -> None:
        self._resolver = resolver or EntityResolver()

    def extract_edges(
        self,
        nodes: list[GraphNode],
        context: dict[str, Any] | None = None,
    ) -> list[GraphEdge]:
        """
        Extract relationship edges from node content and context.

        Args:
            nodes: List of GraphNode objects.
            context: Optional context for LLM-enhanced extraction.

        Returns:
            List of GraphEdge objects.
        """
        context = context or {}
        edges: list[GraphEdge] = []
        node_ids = [n.id for n in nodes]

        # 1. Pattern-based extraction from descriptions
        edges.extend(self._extract_from_text(nodes))

        # 2. Context-based extraction (if query mentions specific entities)
        query = context.get("query", "")
        if query:
            edges.extend(self._extract_from_query(nodes, query))

        # 3. Cross-domain co-occurrence extraction
        edges.extend(self._extract_cooccurrence(nodes))

        # 4. Domain-based dependency extraction
        edges.extend(self._extract_domain_dependencies(nodes))

        # Deduplicate edges
        edges = self._deduplicate_edges(edges)

        return edges

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _extract_from_text(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        """Extract edges from text patterns in node descriptions and properties."""
        edges: list[GraphEdge] = []

        for i, src in enumerate(nodes):
            text = f"{src.name} {src.description}"
            for key, val in src.properties.items():
                text += f" {key} {val}"

            for pattern, relation in _RELATION_PATTERNS:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Try to find the referenced entity in other nodes
                    context_window = text[max(0, match.start() - 50):match.end() + 50].lower()
                    for j, tgt in enumerate(nodes):
                        if i == j:
                            continue
                        tgt_name = tgt.name.lower()
                        if tgt_name in context_window:
                            edges.append(GraphEdge(
                                id=f"edge-{src.id}-{tgt.id}-{relation.value}",
                                source_id=src.id,
                                target_id=tgt.id,
                                relation=relation,
                                weight=0.7,
                                confidence=0.7,
                                evidence=[f"text pattern: {match.group()}"],
                            ))

        return edges

    def _extract_from_query(
        self, nodes: list[GraphNode], query: str
    ) -> list[GraphEdge]:
        """Extract edges implied by the user's query."""
        edges: list[GraphEdge] = []
        query_lower = query.lower()

        # Find nodes mentioned in the query
        mentioned: list[GraphNode] = []
        for node in nodes:
            if node.name.lower() in query_lower:
                mentioned.append(node)

        # Connect mentioned nodes with CORELATION or REFERENCE
        for i, src in enumerate(mentioned):
            for tgt in mentioned[i + 1:]:
                edges.append(GraphEdge(
                    id=f"edge-query-{src.id}-{tgt.id}",
                    source_id=src.id,
                    target_id=tgt.id,
                    relation=RelationType.RELATED_TO,
                    weight=0.8,
                    confidence=0.8,
                    evidence=[f"query co-mention: {query[:100]}"],
                ))

        return edges

    def _extract_cooccurrence(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        """Extract edges based on shared context (same domain or same source)."""
        edges: list[GraphEdge] = []

        # Group by domain
        by_domain: dict[str, list[GraphNode]] = {}
        for node in nodes:
            by_domain.setdefault(node.domain, []).append(node)

        for domain, group in by_domain.items():
            if len(group) > 1:
                # Connect nodes within the same domain
                for i, src in enumerate(group):
                    for tgt in group[i + 1:]:
                        edges.append(GraphEdge(
                            id=f"edge-domain-{src.id}-{tgt.id}",
                            source_id=src.id,
                            target_id=tgt.id,
                            relation=RelationType.RELATED_TO,
                            weight=0.5,
                            confidence=0.5,
                            evidence=[f"same domain: {domain}"],
                        ))

        return edges

    def _extract_domain_dependencies(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        """Extract DEPENDS_ON edges based on known domain relationships."""
        edges: list[GraphEdge] = []

        # Known domain dependency patterns
        dependency_map = {
            "trading": ["data_engineer", "database_engineer", "risk_analyzer"],
            "code_engineer": ["security_engineer", "qa_engineer"],
            "network_engineer": ["security_engineer", "infrastructure_engineer"],
            "devops_assistant": ["infrastructure_engineer", "database_engineer"],
            "system_architect": ["security_engineer", "infrastructure_engineer"],
        }

        for node in nodes:
            deps = dependency_map.get(node.domain, [])
            for dep_domain in deps:
                for tgt in nodes:
                    if tgt.domain == dep_domain and tgt.id != node.id:
                        edges.append(GraphEdge(
                            id=f"edge-dep-{node.id}-{tgt.id}",
                            source_id=node.id,
                            target_id=tgt.id,
                            relation=RelationType.DEPENDS_ON,
                            weight=0.6,
                            confidence=0.6,
                            evidence=[f"domain dependency: {node.domain} → {dep_domain}"],
                        ))

        return edges

    def _deduplicate_edges(self, edges: list[GraphEdge]) -> list[GraphEdge]:
        """Remove duplicate edges (same source, target, relation)."""
        seen: set[tuple[str, str, str]] = set()
        unique: list[GraphEdge] = []

        for edge in edges:
            key = (edge.source_id, edge.target_id, edge.relation.value)
            if key in seen:
                continue
            seen.add(key)
            unique.append(edge)

        return unique
