"""
Capability Contract v1
======================

Frozen schema for Capability Graph v1.

Defines:
- CapabilityNode dataclass (contract schema)
- SubtaskTemplate dataclass (contract schema)
- CAPABILITY_CONTRACT_VERSION
- CapabilityContractError
- Validation functions

CapabilityGraph imports from here.
"""

import re
from dataclasses import dataclass, field
from typing import Any


CAPABILITY_CONTRACT_VERSION = "1.0.0"


class CapabilityContractError(Exception):
    """Raised when a capability or subtask violates the contract."""


@dataclass
class CapabilityNode:
    capability_id: str
    version: str = CAPABILITY_CONTRACT_VERSION
    name: str = ""
    description: str = ""
    required_skills: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    estimated_complexity: str = "medium"
    tags: list[str] = field(default_factory=list)


@dataclass
class SubtaskTemplate:
    subtask_id: str
    name: str
    description: str
    required_skills: list[str] = field(default_factory=list)
    produces_artifact: str = ""
    estimated_duration_minutes: int = 30
    priority: int = 5
    can_parallelize: bool = True


def validate_capability_node(node: CapabilityNode) -> None:
    if not node.capability_id:
        raise CapabilityContractError("capability_id is required")
    if not re.match(r"^[a-z][a-z0-9-]*$", node.capability_id):
        raise CapabilityContractError(f"capability_id '{node.capability_id}' must match ^[a-z][a-z0-9-]*$")
    if not node.name:
        raise CapabilityContractError("name is required")
    if not node.description:
        raise CapabilityContractError("description is required")
    if not node.required_skills:
        raise CapabilityContractError("required_skills must not be empty")
    if not isinstance(node.dependencies, list):
        raise CapabilityContractError("dependencies must be a list")


def validate_subtask_template(template: SubtaskTemplate) -> None:
    if not template.subtask_id:
        raise CapabilityContractError("subtask_id is required")
    if not template.name:
        raise CapabilityContractError("name is required")
    if not template.description:
        raise CapabilityContractError("description is required")
    if not template.required_skills:
        raise CapabilityContractError("required_skills must not be empty")
    if not template.produces_artifact:
        raise CapabilityContractError("produces_artifact is required")
    if template.estimated_duration_minutes <= 0:
        raise CapabilityContractError("estimated_duration_minutes must be > 0")
    if not (1 <= template.priority <= 10):
        raise CapabilityContractError("priority must be between 1 and 10")


def validate_capability_pack(capability_id: str, subtask_templates: list[SubtaskTemplate]) -> None:
    for template in subtask_templates:
        validate_subtask_template(template)
