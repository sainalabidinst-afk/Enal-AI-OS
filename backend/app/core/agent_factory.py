"""
Agent factory for instantiating agents from blueprints.

Transforms persisted agent blueprints into executable runtime instances
by composing existing capability packs, decorators, and connectors.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.core.schemas import AgentBlueprint

logger = logging.getLogger(__name__)


class AgentFactory:
    """Create runtime agent instances from AgentBlueprint definitions."""

    def __init__(self) -> None:
        self._registry: dict[str, type] = {}

    def register(self, name: str, cls: type) -> None:
        self._registry[name] = cls

    def create(self, blueprint: AgentBlueprint | dict[str, Any]) -> Any:
        if isinstance(blueprint, dict):
            blueprint = AgentBlueprint(**blueprint)

        logger.info("Building agent %s from blueprint", blueprint.id)
        base_config = {
            "name": blueprint.name,
            "description": blueprint.description,
            "model": blueprint.model,
            "temperature": blueprint.temperature,
            "max_tokens": blueprint.max_tokens,
            "prompt": blueprint.prompt,
            "tools": list(blueprint.tools),
            "knowledge_base_ids": list(blueprint.knowledge_base_ids),
            "metadata": dict(blueprint.metadata),
        }
        return base_config


agent_factory = AgentFactory()
