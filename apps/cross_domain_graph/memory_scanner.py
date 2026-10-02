"""
Memory Scanner — scans all memory layers for entities and relationships.

Accesses Memory Manager through the shared MemoryContract (ADR-004 compliant),
extracting structured entities from each layer without direct imports.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.cross_domain_graph.schemas import GraphNode, MemoryLayer, NodeType

logger = logging.getLogger(__name__)


class MemoryScanner:
    """
    Scans all ECP memory layers for entities that can be added to the graph.

    Usage::

        scanner = MemoryScanner(memory_manager)
        nodes = scanner.scan_all(["knowledge", "episodic"])
    """

    def __init__(self, memory_manager: Any = None) -> None:
        self._memory_manager = memory_manager

    def _get_memory_manager(self) -> Any:
        """Lazy-load memory manager to avoid import-time coupling."""
        if self._memory_manager is None:
            from backend.app.runtime import memory_manager as _mm
            self._memory_manager = _mm
        return self._memory_manager

    async def scan_layer(
        self,
        layer: str,
        query: str | None = None,
        limit: int = 100,
        project_id: str | None = None,
    ) -> list[GraphNode]:
        """
        Scan a single memory layer for entities.

        Args:
            layer: Memory layer name.
            query: Optional search query.
            limit: Maximum entries to retrieve.
            project_id: Optional project scoping.

        Returns:
            List of GraphNode objects extracted from the layer.
        """
        mm = self._get_memory_manager()
        nodes: list[GraphNode] = []

        try:
            if query:
                entries = await mm.search(layer, query, limit=limit)
            else:
                keys = await mm.list_keys(layer)
                entries = []
                for key in keys[:limit]:
                    val = await mm.retrieve(layer, key)
                    if val:
                        entries.append({"key": key, "value": val})
        except Exception as e:
            logger.warning(f"Failed to scan memory layer '{layer}': {e}")
            return nodes

        for idx, entry in enumerate(entries):
            node = self._extract_node(entry, layer, idx)
            if node:
                nodes.append(node)

        return nodes

    async def scan_all(
        self,
        layers: list[str] | None = None,
        query: str | None = None,
        limit_per_layer: int = 100,
        project_id: str | None = None,
    ) -> list[GraphNode]:
        """
        Scan all specified memory layers.

        Args:
            layers: List of layer names to scan. Defaults to all 7 layers.
            query: Optional search query applied to each layer.
            limit_per_layer: Maximum entries per layer.
            project_id: Optional project scoping.

        Returns:
            Combined list of GraphNode objects from all layers.
        """
        if layers is None:
            layers = [
                MemoryLayer.WORKING.value,
                MemoryLayer.CONVERSATION.value,
                MemoryLayer.KNOWLEDGE.value,
                MemoryLayer.LONGTERM.value,
                MemoryLayer.EPISODIC.value,
                MemoryLayer.SESSION.value,
                MemoryLayer.PROJECT.value,
            ]

        all_nodes: list[GraphNode] = []
        for layer in layers:
            nodes = await self.scan_layer(layer, query, limit_per_layer, project_id)
            all_nodes.extend(nodes)

        return all_nodes

    async def scan_with_context(
        self,
        query: str,
        context: dict[str, Any] | None = None,
    ) -> list[GraphNode]:
        """
        Scan memory layers using a query enriched by context.

        Uses context to prioritize which layers to scan and what to look for.
        """
        context = context or {}
        source_domains = context.get("source_domains", [])  # noqa: F841
        target_layers = context.get("target_memory_layers")

        # If specific layers specified, use them
        if target_layers:
            return await self.scan_all(layers=target_layers, query=query)

        # Otherwise scan all layers
        return await self.scan_all(query=query)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _extract_node(
        self, entry: dict[str, Any], layer: str, idx: int
    ) -> GraphNode | None:
        """Extract a GraphNode from a memory entry."""
        key = entry.get("key", "") if isinstance(entry, dict) else str(entry)
        value = entry.get("value", entry) if isinstance(entry, dict) else entry

        # Normalize value to dict or string
        if isinstance(value, dict):
            name = value.get("name", value.get("title", value.get("description", key)))
            description = value.get("description", value.get("summary", ""))
            node_type_str = value.get("type", value.get("category", "entity"))
            domain = value.get("domain", value.get("pack", "unknown"))
            properties = {k: v for k, v in value.items() if k not in ("name", "description", "type", "domain", "summary", "title")}  # noqa: E501
        elif isinstance(value, str):
            name = value[:100]
            description = value[:500]
            node_type_str = "entity"
            domain = "unknown"
            properties = {}
        else:
            return None

        # Map type string to NodeType enum
        try:
            node_type = NodeType(node_type_str or "entity")
        except ValueError:
            node_type = NodeType.ENTITY

        return GraphNode(
            id=f"{layer}-{idx}-{key[:16]}",
            name=name or f"Entry {idx}",
            node_type=node_type,
            domain=domain or "unknown",
            layer=layer,
            description=str(description)[:500],
            properties=properties,
            confidence=0.5,  # Default; resolver will adjust
        )
