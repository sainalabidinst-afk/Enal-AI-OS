"""
Contract Tests for Capability Contract v1

Ensures all registered capabilities and subtask templates conform
to the frozen Capability Contract v1 schema.
"""

import pytest

from apps.organization.capability_contract import (
    CapabilityContractError,
    validate_capability_node,
    validate_subtask_template,
)
from apps.organization.capability_graph import (
    CapabilityGraph,
    CapabilityNode,
    SubtaskTemplate,
    capability_graph,
)


def test_all_capabilities_have_version():
    for cap_id in capability_graph.get_all_capabilities():
        node = capability_graph.get_capability_node(cap_id)
        assert node is not None
        assert node.version == "1.0.0"


def test_all_capability_ids_match_schema():
    import re
    pattern = re.compile(r"^[a-z][a-z0-9-]*$")
    for cap_id in capability_graph.get_all_capabilities():
        assert pattern.match(cap_id), f"capability_id '{cap_id}' does not match contract schema"


def test_all_capabilities_have_required_fields():
    for cap_id in capability_graph.get_all_capabilities():
        node = capability_graph.get_capability_node(cap_id)
        assert node.name, f"{cap_id}: name is required"
        assert node.description, f"{cap_id}: description is required"
        assert node.required_skills, f"{cap_id}: required_skills must not be empty"


def test_all_subtask_templates_have_required_fields():
    for domain, templates in capability_graph._subtask_templates.items():
        for template in templates:
            assert template.subtask_id, f"{domain}: subtask_id is required"
            assert template.name, f"{domain}: name is required"
            assert template.description, f"{domain}: description is required"
            assert template.required_skills, f"{domain}: required_skills must not be empty"
            assert template.produces_artifact, f"{domain}: produces_artifact is required"
            assert template.estimated_duration_minutes > 0, f"{domain}: estimated_duration_minutes must be > 0"
            assert 1 <= template.priority <= 10, f"{domain}: priority must be between 1 and 10"


def test_validate_capability_node_rejects_missing_fields():
    with pytest.raises(CapabilityContractError):
        validate_capability_node(CapabilityNode(capability_id=""))


def test_validate_capability_node_rejects_invalid_id():
    with pytest.raises(CapabilityContractError):
        validate_capability_node(CapabilityNode(capability_id="InvalidID"))  # uppercase not allowed


def test_validate_subtask_template_rejects_missing_fields():
    with pytest.raises(CapabilityContractError):
        validate_subtask_template(SubtaskTemplate(subtask_id="", name="", description="", produces_artifact=""))


def test_validate_subtask_template_rejects_invalid_duration():
    with pytest.raises(CapabilityContractError):
        validate_subtask_template(SubtaskTemplate(
            subtask_id="x",
            name="X",
            description="X",
            produces_artifact="x",
            estimated_duration_minutes=0,
        ))


def test_validate_subtask_template_rejects_invalid_priority():
    with pytest.raises(CapabilityContractError):
        validate_subtask_template(SubtaskTemplate(
            subtask_id="x",
            name="X",
            description="X",
            produces_artifact="x",
            priority=0,
        ))
    with pytest.raises(CapabilityContractError):
        validate_subtask_template(SubtaskTemplate(
            subtask_id="x",
            name="X",
            description="X",
            produces_artifact="x",
            priority=11,
        ))


def test_capability_graph_instantiation_validates():
    graph = CapabilityGraph()
    assert len(graph.get_all_capabilities()) > 0
