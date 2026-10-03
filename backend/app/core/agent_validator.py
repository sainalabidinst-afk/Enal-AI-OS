"""
Validator for agent blueprints.

Ensures required fields are present and configuration is coherent
before deployment or execution.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.core.schemas import AgentBlueprint

logger = logging.getLogger(__name__)


class AgentValidationError(Exception):
    """Raised when an agent blueprint fails validation."""


class AgentValidator:
    """Validate agent blueprints before runtime execution."""

    def validate(self, blueprint: AgentBlueprint | dict[str, Any]) -> AgentBlueprint:
        if isinstance(blueprint, dict):
            try:
                blueprint = AgentBlueprint(**blueprint)
            except Exception as exc:
                raise AgentValidationError(f"Invalid blueprint schema: {exc}") from exc

        errors: list[str] = []

        if not blueprint.name or not blueprint.name.strip():
            errors.append("Agent name is required")
        if not blueprint.model:
            errors.append("Model selection is required")
        if not blueprint.prompt or not blueprint.prompt.strip():
            errors.append("System prompt is required")
        if blueprint.temperature < 0 or blueprint.temperature > 2:
            errors.append("Temperature must be between 0 and 2")
        if blueprint.max_tokens <= 0:
            errors.append("max_tokens must be greater than 0")

        if errors:
            raise AgentValidationError("; ".join(errors))

        return blueprint


agent_validator = AgentValidator()
