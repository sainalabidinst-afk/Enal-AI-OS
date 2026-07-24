"""
Integration Tests for Workflow Catalog & Resolver
=================================================

Validates the intent-to-workflow resolution flow.

Test scenarios:
    - resolve existing workflow (exact match)
    - unknown intent (not in catalog)
    - duplicate intent detection (rejected at registration)
    - catalog loading (from dict, JSON, file)
    - response contract (ResolveResult fields)
    - resolve_or_raise (exception path)
    - empty intent
    - listing entries
    - find by tag
    - clearing catalog
"""

import json
import tempfile
from pathlib import Path

import pytest

from apps.organization.workflow_catalog import (
    WorkflowCatalog,
    WorkflowCatalogEntry,
    ResolveResult,
    ResolveError,
    CatalogError,
)


@pytest.fixture
def catalog() -> WorkflowCatalog:
    cat = WorkflowCatalog()
    cat.clear()
    return cat


SIMPLE_ENTRY_DICT = {
    "workflow_id": "network-audit-flow",
    "display_name": "Network Security Audit",
    "description": "Run security audit on network devices",
    "supported_intents": ["audit-network", "check-security", "network-scan"],
    "tags": ["network", "security", "audit"],
    "metadata": {"version": "1.0", "domain": "network"},
}

SIMPLE_ENTRY_JSON = json.dumps(SIMPLE_ENTRY_DICT)

DOCS_WORKFLOW_DICT = {
    "workflow_id": "docs-generation-flow",
    "display_name": "Documentation Generation",
    "description": "Generate technical documentation",
    "supported_intents": ["generate-docs", "write-docs", "create-manual"],
    "tags": ["docs", "writing"],
}


def assert_valid_resolve_result(result: ResolveResult) -> None:
    assert isinstance(result, ResolveResult)
    assert isinstance(result.found, bool)
    if result.found:
        assert isinstance(result.workflow_id, str)
        assert isinstance(result.entry, WorkflowCatalogEntry)
        assert result.error is None
        assert isinstance(result.matched_intent, str)
    else:
        assert result.workflow_id is None
        assert result.entry is None
        assert result.error is not None


# -- Tests: Registration / Loading ---


def test_register_entry_directly(catalog: WorkflowCatalog):
    entry = WorkflowCatalogEntry(
        workflow_id="test-flow",
        display_name="Test Flow",
        supported_intents=["test-intent"],
    )
    catalog.register(entry)
    assert catalog.entry_count() == 1
    assert catalog.intent_count() == 1


def test_register_from_dict(catalog: WorkflowCatalog):
    entry = catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    assert entry.workflow_id == "network-audit-flow"
    assert entry.display_name == "Network Security Audit"
    assert len(entry.supported_intents) == 3


def test_register_from_json(catalog: WorkflowCatalog):
    entry = catalog.register_from_json(SIMPLE_ENTRY_JSON)
    assert entry.workflow_id == "network-audit-flow"
    assert len(entry.supported_intents) == 3


def test_register_from_file(catalog: WorkflowCatalog):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(SIMPLE_ENTRY_DICT, f)
        filepath = f.name
    try:
        entry = catalog.register_from_file(filepath)
        assert entry.workflow_id == "network-audit-flow"
        assert len(entry.supported_intents) == 3
    finally:
        Path(filepath).unlink(missing_ok=True)


def test_catalog_loading_workflow_id_required(catalog: WorkflowCatalog):
    with pytest.raises(CatalogError, match="workflow_id is required"):
        catalog.register(WorkflowCatalogEntry(
            workflow_id="", display_name="Bad", supported_intents=["test"],
        ))


def test_catalog_loading_intents_required(catalog: WorkflowCatalog):
    with pytest.raises(CatalogError, match="at least one supported_intent"):
        catalog.register(WorkflowCatalogEntry(
            workflow_id="bad-flow", display_name="Bad", supported_intents=[],
        ))


# -- Tests: Duplicate Detection ---


def test_duplicate_intent_detection(catalog: WorkflowCatalog):
    entry_a = WorkflowCatalogEntry(
        workflow_id="flow-a", display_name="Flow A",
        supported_intents=["shared-intent", "intent-a"],
    )
    catalog.register(entry_a)
    entry_b = WorkflowCatalogEntry(
        workflow_id="flow-b", display_name="Flow B",
        supported_intents=["shared-intent", "intent-b"],
    )
    with pytest.raises(CatalogError, match="Duplicate intent"):
        catalog.register(entry_b)
    assert catalog.entry_count() == 1
    assert catalog.intent_count() == 2


def test_same_intent_same_workflow_allowed(catalog: WorkflowCatalog):
    entry = WorkflowCatalogEntry(
        workflow_id="flow-x", display_name="Flow X",
        supported_intents=["intent-x", "intent-x"],
    )
    catalog.register(entry)
    assert catalog.intent_count() == 1


# -- Tests: Resolution ---


def test_resolve_existing_intent(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    result = catalog.resolve("audit-network")
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert result.error is None
    assert result.matched_intent == "audit-network"
    assert_valid_resolve_result(result)


def test_resolve_multiple_intents_same_workflow(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    for intent in ["audit-network", "check-security", "network-scan"]:
        result = catalog.resolve(intent)
        assert result.found is True
        assert result.workflow_id == "network-audit-flow"
        assert_valid_resolve_result(result)


def test_resolve_unknown_intent(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    result = catalog.resolve("nonexistent-intent")
    assert result.found is False
    assert result.workflow_id is None
    assert result.entry is None
    err = result.error
    assert err is not None
    assert "No workflow found" in err
    assert_valid_resolve_result(result)


def test_resolve_empty_intent(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    result = catalog.resolve("")
    assert result.found is False
    err = result.error
    assert err is not None
    assert "cannot be empty" in err
    assert_valid_resolve_result(result)


def test_resolve_whitespace_intent(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    result = catalog.resolve("   ")
    assert result.found is False
    err = result.error
    assert err is not None
    assert "cannot be empty" in err
    assert_valid_resolve_result(result)


def test_resolve_or_raise_success(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    entry = catalog.resolve_or_raise("audit-network")
    assert entry.workflow_id == "network-audit-flow"


def test_resolve_or_raise_raises_error(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    with pytest.raises(ResolveError, match="No workflow found"):
        catalog.resolve_or_raise("nonexistent")


def test_get_entry_by_workflow_id(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    entry = catalog.get_entry("network-audit-flow")
    assert entry is not None
    assert entry.display_name == "Network Security Audit"
    missing = catalog.get_entry("nonexistent")
    assert missing is None


def test_get_workflow_id_by_intent(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    wf_id = catalog.get_workflow_id("audit-network")
    assert wf_id == "network-audit-flow"
    missing = catalog.get_workflow_id("nonexistent")
    assert missing is None


# -- Tests: Listing & Discovery ---


def test_list_entries(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    catalog.register_from_dict(DOCS_WORKFLOW_DICT)
    entries = catalog.list_entries()
    assert len(entries) == 2
    wf_ids = [e["workflow_id"] for e in entries]
    assert "network-audit-flow" in wf_ids
    assert "docs-generation-flow" in wf_ids


def test_list_intents(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    intents = catalog.list_intents()
    assert len(intents) == 3
    assert intents["audit-network"] == "network-audit-flow"
    assert intents["check-security"] == "network-audit-flow"
    assert intents["network-scan"] == "network-audit-flow"


def test_find_by_tag(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    catalog.register_from_dict(DOCS_WORKFLOW_DICT)
    network_entries = catalog.find_by_tag("network")
    assert len(network_entries) == 1
    assert network_entries[0].workflow_id == "network-audit-flow"
    docs_entries = catalog.find_by_tag("docs")
    assert len(docs_entries) == 1
    assert docs_entries[0].workflow_id == "docs-generation-flow"
    missing_entries = catalog.find_by_tag("nonexistent")
    assert len(missing_entries) == 0


def test_entry_count_and_intent_count(catalog: WorkflowCatalog):
    assert catalog.entry_count() == 0
    assert catalog.intent_count() == 0
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    assert catalog.entry_count() == 1
    assert catalog.intent_count() == 3
    catalog.register_from_dict(DOCS_WORKFLOW_DICT)
    assert catalog.entry_count() == 2
    assert catalog.intent_count() == 6


# -- Tests: Response Contract ---


def test_resolve_result_contract_found(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    result = catalog.resolve("audit-network")
    assert_valid_resolve_result(result)
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert isinstance(result.entry, WorkflowCatalogEntry)
    assert result.error is None
    assert result.matched_intent == "audit-network"
    assert result.entry.workflow_id == "network-audit-flow"
    assert result.entry.display_name == "Network Security Audit"
    assert "audit-network" in result.entry.supported_intents


def test_resolve_result_contract_not_found(catalog: WorkflowCatalog):
    result = catalog.resolve("unknown-intent")
    assert_valid_resolve_result(result)
    assert result.found is False
    assert result.workflow_id is None
    assert result.entry is None
    err = result.error
    assert err is not None
    assert "No workflow found" in err


# -- Tests: Clear ---


def test_clear_catalog(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    assert catalog.entry_count() == 1
    assert catalog.intent_count() == 3
    catalog.clear()
    assert catalog.entry_count() == 0
    assert catalog.intent_count() == 0
    assert catalog.list_entries() == []
    assert catalog.list_intents() == {}


def test_resolve_after_clear(catalog: WorkflowCatalog):
    catalog.register_from_dict(SIMPLE_ENTRY_DICT)
    catalog.clear()
    result = catalog.resolve("audit-network")
    assert result.found is False
    assert_valid_resolve_result(result)
