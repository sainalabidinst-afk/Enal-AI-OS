"""
Cross-Domain Knowledge Graph — Relationship Explorer.

Provides path traversal and explanation between any two entities
in the cross-domain knowledge graph.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.cross_domain_graph.graph_builder import GraphBuilder

logger = logging.getLogger(__name__)


class RelationshipExplorer:
    """Explores and explains relationships between entities in the graph.

    Wraps GraphBuilder.find_path and enhances results with
    human-readable explanations.
    """

    def __init__(self, graph_builder: GraphBuilder) -> None:
        self.builder = graph_builder

    def find_paths(
        self,
        source_entity: str,
        target_entity: str,
        max_depth: int = 5,
    ) -> list[list[Any]]:
        """Find all relationship paths between two entities.

        Args:
            source_entity: Name or partial name of source entity.
            target_entity: Name or partial name of target entity.
            max_depth: Maximum traversal depth.

        Returns:
            List of paths, each path being a list of GraphEdge objects.
        """
        source_nodes = self.builder.query_nodes(query=source_entity)
        target_nodes = self.builder.query_nodes(query=target_entity)

        if not source_nodes or not target_nodes:
            logger.debug(f"Could not find entities: '{source_entity}' or '{target_entity}'")
            return []

        paths = self.builder.find_path(
            source_nodes[0].id,
            target_nodes[0].id,
            max_depth=max_depth,
        )
        return paths

    def explain(
        self,
        source_entity: str,
        target_entity: str,
        max_depth: int = 5,
    ) -> dict[str, Any]:
        """Produce a human-readable explanation of how two entities relate.

        Args:
            source_entity: Name or partial name of source entity.
            target_entity: Name or partial name of target entity.
            max_depth: Maximum traversal depth.

        Returns:
            Dict with explanation text and path descriptions.
        """
        paths = self.find_paths(source_entity, target_entity, max_depth)

        if not paths:
            return {
                "explanation": (
                    f"No path found between '{source_entity}' and '{target_entity}' "
                    f"within {max_depth} hops"
                ),
                "paths": [],
            }

        path_explanations = []
        for path in paths[:3]:
            explanation_parts = []
            for edge in path:
                src = self.builder.get_node(edge.source_id)
                tgt = self.builder.get_node(edge.target_id)
                if src and tgt:
                    explanation_parts.append(
                        f"{src.name} --{edge.relation.value}--> {tgt.name}"
                    )
            path_explanations.append(" | ".join(explanation_parts))

        return {
            "explanation": (
                f"Found {len(paths)} path(s) between '{source_entity}' "
                f"and '{target_entity}'"
            ),
            "paths": path_explanations,
        }

    def circular_dependency_check(self, max_depth: int = 5) -> list[list[str]]:
        """Detect circular dependencies (cycles) in the knowledge graph.

        Args:
            max_depth: Maximum traversal depth for cycle detection.

        Returns:
            List of cycles, each cycle being a list of node names.
        """
        cycles = []
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node_id: str) -> None:
            if node_id in rec_stack:
                cycle_start = path.index(node_id)
                cycle = path[cycle_start:] + [node_id]
                cycles.append([
                    self.builder.get_node(n).name if self.builder.get_node(n) else n
                    for n in cycle
                ])
                return
            if node_id in visited:
                return

            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)

            node = self.builder.get_node(node_id)
            if node:
                for edge in self.builder._edges.values():
                    if edge.source_id == node_id:
                        dfs(edge.target_id)

            path.pop()
            rec_stack.discard(node_id)

        for node_id in list(self.builder._nodes.keys()):
            if node_id not in visited:
                dfs(node_id)

        return cycles
