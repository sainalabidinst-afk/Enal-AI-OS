"""
Validator for tool blueprints.

Ensures tool step graphs are well-formed before execution.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class StepValidationError(Exception):
    """Raised when a tool blueprint fails validation."""


class StepValidator:
    """Validate tool blueprints before runtime execution."""

    def validate(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        errors: list[str] = []

        name = blueprint.get("name")
        if not name or not str(name).strip():
            errors.append("Tool name is required")

        steps = blueprint.get("steps", [])
        if not steps:
            errors.append("At least one step is required")

        seen_ids: set[str] = set()
        for index, step in enumerate(steps):
            step_id = step.get("id")
            if not step_id:
                errors.append(f"Step {index} is missing an id")
            elif step_id in seen_ids:
                errors.append(f"Duplicate step id: {step_id}")
            else:
                seen_ids.add(step_id)

            step_type = step.get("type")
            if not step_type:
                errors.append(f"Step {step_id or index} is missing a type")

        if errors:
            raise StepValidationError("; ".join(errors))

        return blueprint


step_validator = StepValidator()
