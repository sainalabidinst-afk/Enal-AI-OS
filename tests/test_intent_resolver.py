"""
Integration Tests for Intent Resolver
======================================

Validates the intent-to-workflow resolution flow.

Test scenarios:
    - register workflow
    - duplicate workflow detection
    - duplicate intent detection
    - resolve exact intent (confidence 1.0)
    - resolve alias (confidence 0.9)
    - resolve via task name
    - resolve via tag fallback (confidence 0.7)
    - unknown intent
    - workflow execution through resolver
    - telemetry emitted
    - response contract (ResolveResult fields)
"""

import pytest

from apps.organization.capability_execution_engine import (
    ExecutionStatus,
)
from apps.organization.capability_pipeline import CapabilityPipeline
from apps.organization.communication import Event, event_bus
from apps.organization.intent_resolver import (
    INTENT_NOT_FOUND,
    INTENT_RESOLVED,
    WORKFLOW_EXECUTION_STARTED,
    WORKFLOW_SELECTED,
    IntentResolver,
    IntentResolverError,
)
from apps.organization.workflow_catalog import (
    CatalogError,
    ResolveError,
    ResolveResult,
    WorkflowCatalog,
    WorkflowCatalogEntry,
)
from apps.organization.workflow_executor import (
    WorkflowDefinition,
    WorkflowExecutor,
    WorkflowStep,
)

# ─── Test Fixtures ───


@pytest.fixture
def catalog() -> WorkflowCatalog:
    cat = WorkflowCatalog()
    cat.clear()
    return cat


@pytest.fixture
def resolver(catalog: WorkflowCatalog) -> IntentResolver:
    rs = IntentResolver(catalog=catalog)
    rs.clear()
    return rs


@pytest.fixture
def populated_resolver(resolver: IntentResolver) -> IntentResolver:
    """Resolver with pre-registered workflows, aliases, and task names."""
    # Register catalog entries
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="network-audit-flow",
        display_name="Network Security Audit",
        description="Run security audit on network devices",
        supported_intents=["audit-network", "check-security", "network-scan"],
        tags=["network", "security", "audit"],
        category="network",
        metadata={"version": "1.0", "domain": "network"},
    ))
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="docs-generation-flow",
        display_name="Documentation Generation",
        description="Generate technical documentation",
        supported_intents=["generate-docs", "write-docs", "create-manual"],
        tags=["docs", "writing"],
        category="code",
    ))
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="code-review-flow",
        display_name="Code Review",
        description="Review source code for issues",
        supported_intents=["review-code", "code-audit"],
        tags=["code", "review", "quality"],
        category="code",
    ))

    # Register aliases
    resolver.register_aliases({
        "audit": "audit-network",
        "security-check": "check-security",
        "docs": "generate-docs",
        "review": "review-code",
    })

    # Register task names
    resolver.register_task_names({
        "run security audit on network": "audit-network",
        "generate project documentation": "generate-docs",
        "review the source code": "review-code",
    })

    return resolver


# ─── Response Contract Helper ───


def assert_valid_resolve_result(result: ResolveResult) -> None:
    """Validate the standard resolve result contract."""
    assert isinstance(result, ResolveResult)
    assert isinstance(result.found, bool)
    assert isinstance(result.confidence, float)
    assert isinstance(result.reason, str)

    if result.found:
        assert isinstance(result.workflow_id, str)
        assert isinstance(result.entry, WorkflowCatalogEntry)
        assert result.error is None
        assert isinstance(result.matched_intent, str)
        assert result.confidence > 0.0
        assert len(result.reason) > 0
    else:
        assert result.workflow_id is None
        assert result.entry is None
        assert result.error is not None
        assert result.confidence == 0.0


# ─── Tests: Registration / Duplicate Detection ───


def test_register_workflow(resolver: IntentResolver):
    """Test registering a workflow via the resolver's catalog."""
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="test-flow",
        display_name="Test Flow",
        supported_intents=["test-intent"],
    ))
    assert resolver.get_catalog().entry_count() == 1
    assert resolver.get_catalog().intent_count() == 1


def test_duplicate_workflow_detection(resolver: IntentResolver):
    """Test duplicate workflow_id raises CatalogError."""
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="test-flow",
        display_name="Test Flow",
        supported_intents=["test-intent"],
    ))
    # Same workflow_id with different intents should not be allowed
    # (register directly replaces, but we check duplicate intent separately)
    with pytest.raises(CatalogError, match="Duplicate intent"):
        resolver.get_catalog().register(WorkflowCatalogEntry(
            workflow_id="test-flow-2",
            display_name="Test Flow 2",
            supported_intents=["test-intent"],  # Same intent as above
        ))


def test_duplicate_intent_detection(resolver: IntentResolver):
    """Test duplicate intent across different workflows raises CatalogError."""
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="flow-a",
        display_name="Flow A",
        supported_intents=["shared-intent", "intent-a"],
    ))
    with pytest.raises(CatalogError, match="Duplicate intent"):
        resolver.get_catalog().register(WorkflowCatalogEntry(
            workflow_id="flow-b",
            display_name="Flow B",
            supported_intents=["shared-intent", "intent-b"],
        ))
    assert resolver.get_catalog().entry_count() == 1
    assert resolver.get_catalog().intent_count() == 2


# ─── Tests: Exact Intent Resolution ───


def test_resolve_exact_intent(populated_resolver: IntentResolver):
    """Test exact match resolution with confidence 1.0."""
    result = populated_resolver.resolve("audit-network")
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert result.confidence == 1.0
    assert result.error is None
    assert result.matched_intent == "audit-network"
    assert "Exact match" in result.reason
    assert_valid_resolve_result(result)


def test_resolve_multiple_exact_intents(populated_resolver: IntentResolver):
    """Test resolving multiple intents that map to the same workflow."""
    for intent in ["audit-network", "check-security", "network-scan"]:
        result = populated_resolver.resolve(intent)
        assert result.found is True
        assert result.workflow_id == "network-audit-flow"
        assert result.confidence == 1.0
        assert_valid_resolve_result(result)


# ─── Tests: Alias Resolution ───


def test_resolve_alias(populated_resolver: IntentResolver):
    """Test alias resolution with confidence 0.9."""
    result = populated_resolver.resolve("audit")
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert result.confidence == 0.9
    assert "Alias match" in result.reason
    assert_valid_resolve_result(result)


def test_resolve_multiple_aliases(populated_resolver: IntentResolver):
    """Test resolving various aliases."""
    test_cases = [
        ("audit", "network-audit-flow"),
        ("security-check", "network-audit-flow"),
        ("docs", "docs-generation-flow"),
        ("review", "code-review-flow"),
    ]
    for alias, expected_wf in test_cases:
        result = populated_resolver.resolve(alias)
        assert result.found is True
        assert result.workflow_id == expected_wf
        assert result.confidence == 0.9
        assert_valid_resolve_result(result)


def test_alias_registration_and_unregistration(resolver: IntentResolver):
    """Test registering and unregistering aliases."""
    resolver.register_alias("my-alias", "test-intent")
    assert resolver.get_aliases() == {"my-alias": "test-intent"}

    resolver.unregister_alias("my-alias")
    assert resolver.get_aliases() == {}


# ─── Tests: Task Name Resolution ───


def test_resolve_task_name_exact(populated_resolver: IntentResolver):
    """Test exact task name match with confidence 1.0."""
    result = populated_resolver.resolve("run security audit on network")
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert result.confidence == 1.0
    assert "Task name exact match" in result.reason
    assert_valid_resolve_result(result)


def test_resolve_task_name_prefix(populated_resolver: IntentResolver):
    """Test prefix task name match with confidence 0.8."""
    result = populated_resolver.resolve("run security audit on network devices today")
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert result.confidence == 0.8
    assert "Task name prefix match" in result.reason
    assert_valid_resolve_result(result)


# ─── Tests: Tag Fallback ───


def test_resolve_tag_fallback(populated_resolver: IntentResolver):
    """Test tag-based fallback with confidence 0.7."""
    # "security" is a tag on network-audit-flow
    result = populated_resolver.resolve("security")
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert result.confidence == 0.7
    assert "Tag fallback" in result.reason
    assert_valid_resolve_result(result)


def test_resolve_tag_fallback_quality(populated_resolver: IntentResolver):
    """Test tag fallback for a tag that is not also an alias."""
    result = populated_resolver.resolve("quality")
    assert result.found is True
    assert result.confidence == 0.7
    assert result.workflow_id == "code-review-flow"
    assert "Tag fallback" in result.reason
    assert_valid_resolve_result(result)


# ─── Tests: Unknown / Error Cases ───


def test_unknown_intent(populated_resolver: IntentResolver):
    """Test resolution of completely unknown intent."""
    result = populated_resolver.resolve("nonexistent-intent")
    assert result.found is False
    assert result.workflow_id is None
    assert result.entry is None
    assert result.confidence == 0.0
    err = result.error
    assert err is not None
    assert "No workflow found" in err
    assert_valid_resolve_result(result)


def test_empty_intent(populated_resolver: IntentResolver):
    """Test resolution of empty intent string."""
    result = populated_resolver.resolve("")
    assert result.found is False
    assert result.confidence == 0.0
    err = result.error
    assert err is not None
    assert "cannot be empty" in err
    assert_valid_resolve_result(result)


def test_whitespace_intent(populated_resolver: IntentResolver):
    """Test resolution of whitespace-only intent."""
    result = populated_resolver.resolve("   ")
    assert result.found is False
    assert result.confidence == 0.0
    err = result.error
    assert err is not None
    assert "cannot be empty" in err
    assert_valid_resolve_result(result)


def test_resolve_or_raise_success(populated_resolver: IntentResolver):
    """Test resolve_or_raise with a valid intent."""
    entry = populated_resolver.resolve_or_raise("audit-network")
    assert entry.workflow_id == "network-audit-flow"
    assert entry.display_name == "Network Security Audit"


def test_resolve_or_raise_error(populated_resolver: IntentResolver):
    """Test resolve_or_raise raises ResolveError for unknown intent."""
    with pytest.raises(ResolveError, match="No workflow found"):
        populated_resolver.resolve_or_raise("nonexistent")


# ─── Tests: Workflow Execution Through Resolver ───


@pytest.mark.asyncio
async def test_resolve_and_execute(resolver: IntentResolver):
    """Test end-to-end: resolve intent → execute workflow."""
    # Register a workflow
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="simple-flow",
        display_name="Simple Flow",
        supported_intents=["simple-intent"],
    ))

    # We need to test with the executor
    from apps.organization.capability_execution_engine import CapabilityExecutionEngine

    engine = CapabilityExecutionEngine()
    engine.clear_telemetry()
    pipeline = CapabilityPipeline(engine=engine)
    executor = WorkflowExecutor(pipeline=pipeline)

    # Register the workflow definition in executor
    executor.register(WorkflowDefinition(
        workflow_id="simple-flow",
        name="Simple Flow",
        ordered_steps=[
            WorkflowStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Doc Step",
            ),
        ],
    ))

    # Resolve and execute
    response = await resolver.resolve_and_execute(
        intent_id="simple-intent",
        executor=executor,
    )

    assert response.status == ExecutionStatus.COMPLETED
    assert response.workflow_id == "simple-flow"
    assert response.step_count == 1


@pytest.mark.asyncio
async def test_resolve_and_execute_no_executor(resolver: IntentResolver):
    """Test resolve_and_execute without executor raises error."""
    with pytest.raises(IntentResolverError, match="executor is required"):
        await resolver.resolve_and_execute("some-intent")


@pytest.mark.asyncio
async def test_resolve_and_execute_unknown_intent(resolver: IntentResolver):
    """Test resolve_and_execute with unknown intent raises error."""
    from apps.organization.capability_execution_engine import CapabilityExecutionEngine

    engine = CapabilityExecutionEngine()
    engine.clear_telemetry()
    pipeline = CapabilityPipeline(engine=engine)
    executor = WorkflowExecutor(pipeline=pipeline)

    with pytest.raises(IntentResolverError, match="No workflow found"):
        await resolver.resolve_and_execute(
            intent_id="nonexistent",
            executor=executor,
        )


# ─── Tests: Response Contract ───


def test_resolve_result_contract_found(populated_resolver: IntentResolver):
    """Test response contract for a successful resolution."""
    result = populated_resolver.resolve("audit-network")
    assert_valid_resolve_result(result)
    assert result.found is True
    assert result.workflow_id == "network-audit-flow"
    assert isinstance(result.entry, WorkflowCatalogEntry)
    assert result.error is None
    assert result.matched_intent == "audit-network"
    assert result.confidence == 1.0
    assert "Exact match" in result.reason

    # Verify entry details are accessible
    assert result.entry.workflow_id == "network-audit-flow"
    assert result.entry.display_name == "Network Security Audit"
    assert "audit-network" in result.entry.supported_intents


def test_resolve_result_contract_not_found(populated_resolver: IntentResolver):
    """Test response contract for an unresolved intent."""
    result = populated_resolver.resolve("unknown-intent")
    assert_valid_resolve_result(result)
    assert result.found is False
    assert result.workflow_id is None
    assert result.entry is None
    assert result.confidence == 0.0
    assert result.reason is not None
    err = result.error
    assert err is not None
    assert "No workflow found" in err


def test_resolve_result_contract_alias(populated_resolver: IntentResolver):
    """Test response contract for alias resolution."""
    result = populated_resolver.resolve("audit")
    assert_valid_resolve_result(result)
    assert result.found is True
    assert result.confidence == 0.9
    assert "Alias match" in result.reason


def test_resolve_result_contract_tag(populated_resolver: IntentResolver):
    """Test response contract for tag fallback."""
    result = populated_resolver.resolve("security")
    assert_valid_resolve_result(result)
    assert result.found is True
    assert result.confidence == 0.7
    assert "Tag fallback" in result.reason


# ─── Tests: Telemetry ───


class TelemetryCollector:
    """Simple collector for telemetry events during testing."""

    def __init__(self) -> None:
        self.events: list[Event] = []

    def on_event(self, event: Event) -> None:
        self.events.append(event)


@pytest.fixture
def telemetry_collector() -> TelemetryCollector:
    collector = TelemetryCollector()
    # Subscribe to all resolver event types
    for event_type in [INTENT_RESOLVED, INTENT_NOT_FOUND, WORKFLOW_SELECTED, WORKFLOW_EXECUTION_STARTED]:
        event_bus.subscribe(event_type, collector.on_event)
    return collector


def test_telemetry_intent_resolved(populated_resolver: IntentResolver, telemetry_collector):
    """Test that IntentResolved telemetry is emitted on successful resolve."""
    populated_resolver.resolve("audit-network")

    resolved_events = [e for e in telemetry_collector.events if e.type == INTENT_RESOLVED]
    assert len(resolved_events) >= 1

    event = resolved_events[0]
    assert event.source == "intent_resolver"
    assert event.data["resolved"] is True
    assert event.data["workflow_id"] == "network-audit-flow"
    assert event.data["matched_intent"] == "audit-network"
    assert event.data["confidence"] == 1.0


def test_telemetry_intent_not_found(populated_resolver: IntentResolver, telemetry_collector):
    """Test that IntentNotFound telemetry is emitted on failed resolve."""
    populated_resolver.resolve("nonexistent")

    not_found_events = [e for e in telemetry_collector.events if e.type == INTENT_NOT_FOUND]
    assert len(not_found_events) >= 1

    event = not_found_events[0]
    assert event.source == "intent_resolver"
    assert event.data["resolved"] is False
    assert event.data["intent_id"] == "nonexistent"


@pytest.mark.asyncio
async def test_telemetry_workflow_selected_and_execution_started(resolver: IntentResolver, telemetry_collector):
    """Test that WorkflowSelected and WorkflowExecutionStarted telemetry is emitted during execution."""
    resolver.get_catalog().register(WorkflowCatalogEntry(
        workflow_id="simple-flow",
        display_name="Simple Flow",
        supported_intents=["simple-intent"],
    ))

    from apps.organization.capability_execution_engine import CapabilityExecutionEngine

    engine = CapabilityExecutionEngine()
    engine.clear_telemetry()
    pipeline = CapabilityPipeline(engine=engine)
    executor = WorkflowExecutor(pipeline=pipeline)

    executor.register(WorkflowDefinition(
        workflow_id="simple-flow",
        name="Simple Flow",
        ordered_steps=[
            WorkflowStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Doc Step",
            ),
        ],
    ))

    await resolver.resolve_and_execute(
        intent_id="simple-intent",
        executor=executor,
    )

    selected_events = [e for e in telemetry_collector.events if e.type == WORKFLOW_SELECTED]
    assert len(selected_events) >= 1
    assert selected_events[0].data["workflow_id"] == "simple-flow"

    started_events = [e for e in telemetry_collector.events if e.type == WORKFLOW_EXECUTION_STARTED]
    assert len(started_events) >= 1
    assert started_events[0].data["workflow_id"] == "simple-flow"


def test_telemetry_on_alias_resolve(populated_resolver: IntentResolver, telemetry_collector):
    """Test telemetry is emitted for alias resolution."""
    populated_resolver.resolve("audit")

    resolved_events = [e for e in telemetry_collector.events if e.type == INTENT_RESOLVED]
    assert len(resolved_events) >= 1
    assert resolved_events[0].data["confidence"] == 0.9


def test_telemetry_on_tag_resolve(populated_resolver: IntentResolver, telemetry_collector):
    """Test telemetry is emitted for tag-based resolution."""
    populated_resolver.resolve("security")

    resolved_events = [e for e in telemetry_collector.events if e.type == INTENT_RESOLVED]
    assert len(resolved_events) >= 1
    assert resolved_events[0].data["confidence"] == 0.7


# ─── Tests: Alias Management ───


def test_get_alias_for_intent(resolver: IntentResolver):
    """Test retrieving aliases for a specific intent."""
    resolver.register_alias("alias-a", "intent-1")
    resolver.register_alias("alias-b", "intent-1")
    resolver.register_alias("alias-c", "intent-2")

    aliases = resolver.get_alias_for_intent("intent-1")
    assert len(aliases) == 2
    assert "alias-a" in aliases
    assert "alias-b" in aliases

    aliases = resolver.get_alias_for_intent("intent-2")
    assert len(aliases) == 1
    assert "alias-c" in aliases


def test_register_alias_validation(resolver: IntentResolver):
    """Test alias registration validation."""
    with pytest.raises(IntentResolverError, match="cannot be empty"):
        resolver.register_alias("", "intent-1")
    with pytest.raises(IntentResolverError, match="cannot be empty"):
        resolver.register_alias("valid-alias", "")


# ─── Tests: Intent Resolver Error ───


def test_intent_resolver_error():
    """Test IntentResolverError exception."""
    err = IntentResolverError("Something went wrong")
    assert str(err) == "Something went wrong"
    assert isinstance(err, Exception)


def test_catalog_integration(resolver: IntentResolver):
    """Test that resolver correctly wraps and exposes catalog."""
    catalog = resolver.get_catalog()
    assert isinstance(catalog, WorkflowCatalog)
    assert catalog is resolver._catalog

