"""
Entity Resolver — identifies the same entity across domains and layers.

Resolves potential duplicates and assigns canonical IDs to entities
that refer to the same real-world concept, even when stored in
different memory layers or described differently.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.cross_domain_graph.schemas import GraphNode, NodeType, ResolvedEntity

logger = logging.getLogger(__name__)


class EntityResolver:
    """
    Resolves entities across domains and memory layers.

    Usage::

        resolver = EntityResolver()
        resolved = resolver.resolve(nodes)
        graph_nodes = resolver.build_resolved_nodes(nodes, resolved)
    """

    # Common name normalization patterns
    _STOP_WORDS = {"the", "a", "an", "of", "in", "on", "at", "for", "to", "and", "or"}
    _NORMALIZE_PATTERN = re.compile(r"[^\w\s]")

    def __init__(self, confidence_threshold: float = 0.7) -> None:
        self.confidence_threshold = confidence_threshold

    def resolve(self, nodes: list[GraphNode]) -> list[ResolvedEntity]:
        """
        Resolve entities across nodes, identifying duplicates.

        Args:
            nodes: List of GraphNode objects from the scanner.

        Returns:
            List of ResolvedEntity objects with canonical IDs and aliases.
        """
        groups: list[list[GraphNode]] = []
        assigned: set[str] = set()

        for node in nodes:
            if node.id in assigned:
                continue

            similar = self._find_similar(node, [n for n in nodes if n.id not in assigned])
            group = [node] + similar

            for n in group:
                assigned.add(n.id)

            canonical = self._select_canonical(group)
            aliases = [n.name for n in group if n.name != canonical.name]

            groups.append(group)

            yield ResolvedEntity(
                canonical_id=canonical.id,
                name=canonical.name,
                domain=canonical.domain,
                layer=canonical.layer,
                aliases=aliases,
                confidence=self._group_confidence(group),
            )

    def resolve_all(self, nodes: list[GraphNode]) -> list[ResolvedEntity]:
        """Convenience method: collect all resolved entities into a list."""
        return list(self.resolve(nodes))

    def build_canonical_nodes(
        self,
        original_nodes: list[GraphNode],
        resolved: list[ResolvedEntity],
    ) -> list[GraphNode]:
        """
        Build a deduplicated set of GraphNodes using canonical IDs.

        Nodes that are resolved to the same entity are merged into the
        canonical node, with other layers/domains noted as aliases.
        """
        canonical_map: dict[str, GraphNode] = {}
        node_by_id = {n.id: n for n in original_nodes}

        for entity in resolved:
            canonical = node_by_id.get(entity.canonical_id)
            if canonical is None:
                continue

            # Create a new node with canonical ID, merging properties
            merged = GraphNode(
                id=entity.canonical_id,
                name=entity.name,
                node_type=canonical.node_type,
                domain=canonical.domain,
                layer=canonical.layer,
                description=canonical.description,
                properties={
                    **canonical.properties,
                    "alias_domains": entity.aliases,
                    "resolved_from_layers": [entity.layer],
                    "resolution_confidence": entity.confidence,
                },
                confidence=max(canonical.confidence, entity.confidence),
            )
            canonical_map[entity.canonical_id] = merged

        return list(canonical_map.values())

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _find_similar(self, target: GraphNode, candidates: list[GraphNode]) -> list[GraphNode]:
        """Find nodes similar to target using name and description similarity."""
        target_norm = self._normalize_name(target.name)
        results: list[GraphNode] = []

        for candidate in candidates:
            if candidate.id == target.id:
                continue

            # Exact name match (case-insensitive)
            if self._normalize_name(candidate.name) == target_norm:
                results.append(candidate)
                continue

            # Substring match
            if target_norm in self._normalize_name(candidate.name):
                results.append(candidate)
                continue

            # Description overlap
            if self._description_similarity(target.description, candidate.description) > 0.5:
                results.append(candidate)

        return results

    def _normalize_name(self, name: str) -> str:
        """Normalize a name for comparison."""
        lowered = name.lower()
        tokens = [t for t in lowered.split() if t not in self._STOP_WORDS]
        return " ".join(tokens)

    def _description_similarity(self, desc1: str, desc2: str) -> float:
        """Compute Jaccard similarity between description token sets."""
        if not desc1 or not desc2:
            return 0.0

        tokens1 = set(self._normalize_name(desc1).split())
        tokens2 = set(self._normalize_name(desc2).split())

        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1 & tokens2
        union = tokens1 | tokens2

        return len(intersection) / len(union)

    def _select_canonical(self, group: list[GraphNode]) -> GraphNode:
        """Select the canonical node from a group of similar nodes."""
        # Prefer knowledge layer nodes as canonical
        for node in sorted(group, key=lambda n: (
            n.layer != "knowledge",  # knowledge first
            n.layer != "project",    # project second
            -n.confidence,           # higher confidence first
        )):
            return node
        return group[0]

    def _group_confidence(self, group: list[GraphNode]) -> float:
        """Compute confidence for a resolved entity group."""
        if len(group) == 1:
            return group[0].confidence

        # Higher confidence when multiple sources agree on the same entity
        avg_conf = sum(n.confidence for n in group) / len(group)
        agreement_bonus = min(0.3, 0.05 * (len(group) - 1))

        return min(1.0, round(avg_conf + agreement_bonus, 4))
