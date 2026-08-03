import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from backend.app.core.mcp_registry import mcp_registry
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


class EntityType(str, Enum):
    TOOL = "tool"
    RESOURCE = "resource"
    SERVICE = "service"
    CONCEPT = "concept"
    WORKFLOW = "workflow"


@dataclass
class WorldEntity:
    id: str
    name: str
    entity_type: EntityType
    description: str
    properties: dict[str, Any] = field(default_factory=dict)
    relationships: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorldModel:
    entities: dict[str, WorldEntity] = field(default_factory=dict)
    relations: list[dict[str, Any]] = field(default_factory=list)


class WorldModelEngine:
    def __init__(self):
        self._model = WorldModel()
        self._initialize_from_tools()

    def _initialize_from_tools(self):
        for tool in mcp_registry.all_schemas():
            entity = WorldEntity(
                id=tool["function"]["name"],
                name=tool["function"]["name"],
                entity_type=EntityType.TOOL,
                description=tool["function"]["description"],
                properties=tool["function"].get("parameters", {}),
            )
            self._model.entities[entity.id] = entity

    async def query(self, query: str) -> list[dict[str, Any]]:
        entities = list(self._model.entities.values())
        relevant = []
        query_lower = query.lower()
        for entity in entities:
            if query_lower in entity.name.lower() or query_lower in entity.description.lower():
                relevant.append({
                    "id": entity.id,
                    "name": entity.name,
                    "type": entity.entity_type.value,
                    "description": entity.description,
                    "properties": entity.properties,
                })
        return relevant[:5]

    async def infer(self, context: str) -> dict[str, Any]:
        prompt = (
            "Given the current context and available tools, infer what entities and relationships are relevant.\n"
            f"Context: {context}\n\n"
            "Available entities: " + ", ".join(self._model.entities.keys())[:500] + "\n\n"
            "Output JSON: {\"relevant_entities\": [str], \"suggested_actions\": [str], \"confidence\": float}"
        )
        response = await model_router.acomplete([{"role": "user", "content": prompt}], temperature=0.3, max_tokens=512)
        try:
            return json.loads(response.choices[0].message.content)
        except (json.JSONDecodeError, AttributeError):
            return {"relevant_entities": [], "suggested_actions": [], "confidence": 0.0}

    def get_entity(self, entity_id: str) -> WorldEntity | None:
        return self._model.entities.get(entity_id)

    def add_entity(self, entity: WorldEntity):
        self._model.entities[entity.id] = entity


world_model = WorldModelEngine()
