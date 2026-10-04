"""
Template Registry
==================

Pre-built agent, tool, and voice templates for the Marketplace.
Templates are stored as JSON files in the ``templates/`` directory and
loaded at startup, providing a rich set of ready-to-use blueprints.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


@dataclass
class TemplateMetadata:
    """Metadata for a marketplace template."""

    author: str = "Enal-AI-OS"
    version: str = "1.0.0"
    rating: float = 0.0
    clones: int = 0
    created_at: str = ""
    updated_at: str = ""


@dataclass
class AgentTemplate:
    """Pre-built agent template."""

    id: str
    name: str
    description: str
    category: str
    tags: list[str]
    type: str
    config: dict[str, Any]
    metadata: TemplateMetadata = field(default_factory=TemplateMetadata)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "type": self.type,
            "config": self.config,
            "author": self.metadata.author,
            "version": self.metadata.version,
            "rating": self.metadata.rating,
            "clones": self.metadata.clones,
            "created_at": self.metadata.created_at,
            "updated_at": self.metadata.updated_at,
        }


class TemplateRegistry:
    """Registry of pre-built templates for the Marketplace.

    Loads template definitions from JSON files at startup and provides
    lookup, filtering, and search capabilities.
    """

    def __init__(self, template_dir: str | None = None) -> None:
        self._templates: dict[str, AgentTemplate] = {}
        self._template_dir = template_dir or TEMPLATE_DIR
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all template JSON files from the template directory."""
        if not os.path.isdir(self._template_dir):
            logger.warning("Template directory not found: %s", self._template_dir)
            return

        for filename in sorted(os.listdir(self._template_dir)):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self._template_dir, filename)
            try:
                with open(filepath, encoding="utf-8") as f:
                    data = json.load(f)
                metadata = TemplateMetadata(**data.get("metadata", {}))
                template = AgentTemplate(
                    id=data["id"],
                    name=data["name"],
                    description=data["description"],
                    category=data["category"],
                    tags=data.get("tags", []),
                    type=data.get("type", "agent"),
                    config=data.get("config", {}),
                    metadata=metadata,
                )
                self._templates[template.id] = template
                logger.debug("Loaded template: %s (%s)", template.name, template.id)
            except Exception as exc:
                logger.error("Failed to load template %s: %s", filename, exc)

        logger.info("Loaded %d templates from %s", len(self._templates), self._template_dir)

    def list_templates(self) -> list[AgentTemplate]:
        """Return all registered templates."""
        return list(self._templates.values())

    def get_template(self, template_id: str) -> AgentTemplate | None:
        """Retrieve a specific template by ID."""
        return self._templates.get(template_id)

    def list_by_category(self, category: str) -> list[AgentTemplate]:
        """Return templates filtered by category."""
        return [t for t in self._templates.values() if t.category.lower() == category.lower()]

    def search(self, query: str) -> list[AgentTemplate]:
        """Search templates by name, description, or tags."""
        query_lower = query.lower()
        results = []
        for template in self._templates.values():
            if (
                query_lower in template.name.lower()
                or query_lower in template.description.lower()
                or any(query_lower in tag.lower() for tag in template.tags)
            ):
                results.append(template)
        return results

    def clone_template(self, template_id: str) -> dict[str, Any]:
        """Produce a cloneable config from a template (with fresh ID)."""
        template = self._templates.get(template_id)
        if template is None:
            return None
        config = dict(template.config)
        config["template_id"] = template_id
        config["template_name"] = template.name
        return {
            "id": str(uuid4()),
            "template_id": template_id,
            "name": f"{template.name} (Clone)",
            "description": template.description,
            "category": template.category,
            "tags": template.tags,
            "type": template.type,
            "config": config,
        }


template_registry = TemplateRegistry()
