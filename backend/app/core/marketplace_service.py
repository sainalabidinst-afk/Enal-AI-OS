"""
Marketplace services for sharing and discovering agents/tools.

Provides template registry, sharing, cloning, and analytics.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class MarketplaceService:
    """Marketplace service for managing shared agents and tools."""

    def __init__(self) -> None:
        self._listings: dict[str, dict[str, Any]] = {}
        self._clones: dict[str, list[dict[str, Any]]] = {}
        self._analytics: dict[str, dict[str, Any]] = {}

    def share(self, agent_id: str, config: dict[str, Any]) -> dict[str, Any]:
        listing = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "name": config.get("name", agent_id),
            "description": config.get("description", ""),
            "category": config.get("category", "Agent"),
            "author": config.get("author", "Enal-AI-OS"),
            "tags": config.get("tags", []),
            "rating": config.get("rating", 0.0),
            "config": config,
            "created_at": datetime.now(UTC).isoformat(),
            "status": "active",
        }
        self._listings[agent_id] = listing
        logger.info("Shared agent %s: %s", agent_id, listing["id"])
        return listing

    def unshare(self, agent_id: str) -> bool:
        if agent_id in self._listings:
            del self._listings[agent_id]
            return True
        return False

    def get_listing(self, agent_id: str) -> dict[str, Any] | None:
        return self._listings.get(agent_id)

    def list_listings(self) -> list[dict[str, Any]]:
        return [
            {
                "id": listing["id"],
                "agent_id": listing["agent_id"],
                "name": listing.get("name", listing["agent_id"]),
                "description": listing.get("description", ""),
                "category": listing.get("category", "Agent"),
                "author": listing.get("author", "Enal-AI-OS"),
                "tags": listing.get("tags", []),
                "rating": listing.get("rating", 0.0),
                "created_at": listing.get("created_at", ""),
                "status": listing.get("status", "active"),
            }
            for listing in self._listings.values()
        ]

    def record_clone(self, agent_id: str, user_id: str) -> None:
        clone_event = {
            "agent_id": agent_id,
            "user_id": user_id,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        self._clones.setdefault(agent_id, []).append(clone_event)
        self._analytics.setdefault(agent_id, {"clones": 0, "views": 0})
        self._analytics[agent_id]["clones"] += 1

    def record_view(self, agent_id: str) -> None:
        self._analytics.setdefault(agent_id, {"clones": 0, "views": 0})
        self._analytics[agent_id]["views"] += 1

    def get_analytics(self, agent_id: str) -> dict[str, Any]:
        return self._analytics.get(agent_id, {"clones": 0, "views": 0})


marketplace_service = MarketplaceService()
