"""
Intent Resolver
================

Deterministic resolver for mapping intents/task names to registered workflows.

Resolver BUKAN AI Planner.
Resolver TIDAK membuat workflow baru.
Resolver TIDAK melakukan reasoning.
Resolver hanya melakukan pencarian workflow yang telah terdaftar
menggunakan aturan deterministik.

Resolution strategies (in order of precedence):
    1. Exact match on intent_id → confidence 1.0
    2. Alias match → confidence 0.9
    3. Task name match → confidence 1.0 (if exact), 0.8 (if partial)
    4. Tag-based fallback → confidence 0.7

Flow:
    Intent ID / Task Name
        ↓
    IntentResolver.resolve(intent_id)
        ↓
    ┌── Exact match? ──→ ResolveResult(confidence=1.0)
    ├── Alias match? ──→ ResolveResult(confidence=0.9)
    ├── Task name match? ──→ ResolveResult(confidence=1.0/0.8)
    ├── Tag fallback? ──→ ResolveResult(confidence=0.7)
    └── Not found ──→ ResolveResult(found=False)
"""

import logging
from typing import Any

from apps.organization.communication import Event, event_bus
from apps.organization.workflow_catalog import (
    ResolveError,
    WorkflowCatalog,
    WorkflowCatalogEntry,
    workflow_catalog,
)
from apps.organization.workflow_catalog import (
    ResolveResult as CatalogResolveResult,
)

logger = logging.getLogger(__name__)

# ─── Telemetry Event Types ───

INTENT_RESOLVED = "IntentResolved"
INTENT_NOT_FOUND = "IntentNotFound"
WORKFLOW_SELECTED = "WorkflowSelected"
WORKFLOW_EXECUTION_STARTED = "WorkflowExecutionStarted"

# ─── Error ───


class IntentResolverError(Exception):
    """Raised when the resolver encounters an error."""


# ─── Resolver ───


class IntentResolver:
    """Deterministic resolver that maps intents/task names to registered workflows.

    Uses only exact match, alias lookup, and tag-based fallback.
    Does NOT use LLM, semantic search, embeddings, or reasoning.

    The resolver wraps a WorkflowCatalog and adds:
        - Alias system (intent aliases for flexible matching)
        - Task name resolution
        - Tag-based fallback
        - Telemetry events (via EventBus)
        - Integration with WorkflowExecutor for end-to-end execution
    """

    def __init__(
        self,
        catalog: WorkflowCatalog | None = None,
    ):
        self._catalog = catalog or workflow_catalog
        self._aliases: dict[str, str] = {}  # alias → intent_id
        self._task_name_index: dict[str, str] = {}  # task_name → intent_id

    # ─── Alias Management ───

    def register_alias(self, alias: str, intent_id: str) -> None:
        """Register an alias that maps to an intent_id.

        Args:
            alias: The alias string (e.g., "audit" → "audit-network").
            intent_id: The canonical intent_id this alias points to.

        Raises:
            IntentResolverError: If alias is empty.
        """
        if not alias or not alias.strip():
            raise IntentResolverError("Alias cannot be empty")
        if not intent_id or not intent_id.strip():
            raise IntentResolverError("intent_id cannot be empty")

        self._aliases[alias.strip()] = intent_id.strip()
        logger.info("Alias registered: '%s' → '%s'", alias, intent_id)

    def register_aliases(self, alias_map: dict[str, str]) -> None:
        """Register multiple aliases at once.

        Args:
            alias_map: Dictionary mapping aliases to intent_ids.
        """
        for alias, intent_id in alias_map.items():
            self.register_alias(alias, intent_id)

    def unregister_alias(self, alias: str) -> None:
        """Remove an alias registration."""
        self._aliases.pop(alias, None)
        logger.info("Alias unregistered: '%s'", alias)

    def get_aliases(self) -> dict[str, str]:
        """Get all registered aliases."""
        return dict(self._aliases)

    def get_alias_for_intent(self, intent_id: str) -> list[str]:
        """Get all aliases that point to a specific intent_id."""
        return [alias for alias, target in self._aliases.items() if target == intent_id]

    # ─── Task Name Registration ───

    def register_task_name(self, task_name: str, intent_id: str) -> None:
        """Register a task name that maps to an intent_id.

        Task names provide a more descriptive way to reference intents
        (e.g., "run network security audit" → "audit-network").

        Args:
            task_name: The task description or name.
            intent_id: The canonical intent_id this task maps to.
        """
        if not task_name or not task_name.strip():
            raise IntentResolverError("task_name cannot be empty")

        normalized = task_name.strip().lower()
        self._task_name_index[normalized] = intent_id.strip()
        logger.info("Task name registered: '%s' → '%s'", task_name, intent_id)

    def register_task_names(self, task_map: dict[str, str]) -> None:
        """Register multiple task names at once."""
        for task_name, intent_id in task_map.items():
            self.register_task_name(task_name, intent_id)

    def unregister_task_name(self, task_name: str) -> None:
        """Remove a task name registration."""
        normalized = task_name.strip().lower()
        self._task_name_index.pop(normalized, None)
        logger.info("Task name unregistered: '%s'", task_name)

    # ─── Resolution ───

    def resolve(self, intent_id: str) -> CatalogResolveResult:
        """Resolve an intent_id to a workflow using deterministic rules.

        Resolution strategy (in order):
            1. Exact match on intent_id (via catalog)
            2. Alias match (alias → intent_id → catalog)
            3. Task name match (exact or prefix)
            4. Tag-based fallback (lowest confidence)

        Args:
            intent_id: The intent or task identifier to resolve.

        Returns:
            ResolveResult with standardized fields.
        """
        if not intent_id or not intent_id.strip():
            return CatalogResolveResult(
                found=False,
                workflow_id=None,
                entry=None,
                error="Intent cannot be empty",
                confidence=0.0,
                reason="Empty intent provided",
            )

        intent_id = intent_id.strip()

        # ── Strategy 1: Exact match via catalog ──
        cat_result = self._catalog.resolve(intent_id)
        if cat_result.found:
            # Enhance with confidence and reason
            result = CatalogResolveResult(
                found=True,
                workflow_id=cat_result.workflow_id,
                entry=cat_result.entry,
                error=None,
                matched_intent=intent_id,
                confidence=1.0,
                reason=f"Exact match: intent '{intent_id}' → workflow '{cat_result.workflow_id}'",
            )
            self._emit_resolved(result)
            return result

        # ── Strategy 2: Alias match ──
        target_intent = self._aliases.get(intent_id)
        if target_intent:
            cat_result = self._catalog.resolve(target_intent)
            if cat_result.found:
                result = CatalogResolveResult(
                    found=True,
                    workflow_id=cat_result.workflow_id,
                    entry=cat_result.entry,
                    error=None,
                    matched_intent=target_intent,
                    confidence=0.9,
                    reason=f"Alias match: '{intent_id}' → '{target_intent}' → workflow '{cat_result.workflow_id}'",
                )
                self._emit_resolved(result)
                return result

        # ── Strategy 3: Task name match ──
        normalized = intent_id.lower()
        # 3a: Exact task name match
        task_intent = self._task_name_index.get(normalized)
        if task_intent:
            cat_result = self._catalog.resolve(task_intent)
            if cat_result.found:
                result = CatalogResolveResult(
                    found=True,
                    workflow_id=cat_result.workflow_id,
                    entry=cat_result.entry,
                    error=None,
                    matched_intent=task_intent,
                    confidence=1.0,
                    reason=f"Task name exact match: '{intent_id}' → '{task_intent}' → workflow '{cat_result.workflow_id}'",
                )
                self._emit_resolved(result)
                return result

        # 3b: Prefix task name match (find longest matching prefix)
        matching_tasks = [tn for tn in self._task_name_index if normalized.startswith(tn)]
        if matching_tasks:
            # Pick the longest matching prefix
            best_task = max(matching_tasks, key=len)
            task_intent = self._task_name_index[best_task]
            cat_result = self._catalog.resolve(task_intent)
            if cat_result.found:
                result = CatalogResolveResult(
                    found=True,
                    workflow_id=cat_result.workflow_id,
                    entry=cat_result.entry,
                    error=None,
                    matched_intent=task_intent,
                    confidence=0.8,
                    reason=f"Task name prefix match: '{intent_id}' starts with '{best_task}' → '{task_intent}' → workflow '{cat_result.workflow_id}'",
                )
                self._emit_resolved(result)
                return result

        # ── Strategy 4: Tag-based fallback ──
        # Check if intent_id looks like a tag and find workflows with matching tags
        tag_entries = self._catalog.find_by_tag(intent_id)
        if tag_entries:
            entry = tag_entries[0]  # Pick the first match
            result = CatalogResolveResult(
                found=True,
                workflow_id=entry.workflow_id,
                entry=entry,
                error=None,
                matched_intent=intent_id,
                confidence=0.7,
                reason=f"Tag fallback: intent '{intent_id}' matches tag → workflow '{entry.workflow_id}'",
            )
            self._emit_resolved(result)
            return result

        # ── Not found ──
        result = CatalogResolveResult(
            found=False,
            workflow_id=None,
            entry=None,
            error=f"No workflow found for intent: '{intent_id}'",
            matched_intent=None,
            confidence=0.0,
            reason=f"Intent '{intent_id}' not found via any resolution strategy",
        )
        self._emit_not_found(intent_id, result)
        return result

    def resolve_or_raise(self, intent_id: str) -> WorkflowCatalogEntry:
        """Resolve an intent or raise ResolveError if not found.

        Args:
            intent_id: The intent/task identifier to resolve.

        Returns:
            WorkflowCatalogEntry matching the intent.

        Raises:
            ResolveError: If no workflow matches the intent.
        """
        result = self.resolve(intent_id)
        if not result.found:
            raise ResolveError(intent_id, result.error)
        return result.entry  # type: ignore[return-value]

    # ─── Execution Integration ───

    async def resolve_and_execute(
        self,
        intent_id: str,
        input_data: dict[str, Any] | None = None,
        executor: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Resolve an intent and execute the matched workflow.

        This is the main integration helper that connects:
            Intent → Resolver → WorkflowExecutor → CapabilityPipeline → ExecutionEngine

        Args:
            intent_id: The intent/task identifier to resolve.
            input_data: Optional input data for workflow execution.
            executor: The WorkflowExecutor instance to use.
            **kwargs: Additional arguments passed to executor.execute().

        Returns:
            WorkflowResponse from the execution.

        Raises:
            IntentResolverError: If resolution fails or no executor provided.
        """
        if executor is None:
            raise IntentResolverError("executor is required for resolve_and_execute")

        # 1. Resolve intent to workflow
        result = self.resolve(intent_id)
        if not result.found:
            raise IntentResolverError(
                f"Cannot execute: {result.error}"
            )

        # 2. Emit WorkflowSelected telemetry
        self._emit_workflow_selected(result)

        # 3. Emit WorkflowExecutionStarted telemetry
        self._emit_execution_started(result, input_data)

        # 4. Execute the workflow
        response = await executor.execute(
            result.workflow_id,
            input_data=input_data,
            **kwargs,
        )

        return response

    # ─── Telemetry Events ───

    def _emit_resolved(self, result: CatalogResolveResult) -> None:
        """Emit IntentResolved telemetry event."""
        event = Event(
            event_type=INTENT_RESOLVED,
            source="intent_resolver",
            data={
                "resolved": True,
                "workflow_id": result.workflow_id,
                "matched_intent": result.matched_intent,
                "confidence": result.confidence,
                "reason": result.reason,
            },
        )
        event_bus.publish(event)

    def _emit_not_found(self, intent_id: str, result: CatalogResolveResult) -> None:
        """Emit IntentNotFound telemetry event."""
        event = Event(
            event_type=INTENT_NOT_FOUND,
            source="intent_resolver",
            data={
                "resolved": False,
                "intent_id": intent_id,
                "error": result.error,
            },
        )
        event_bus.publish(event)

    def _emit_workflow_selected(self, result: CatalogResolveResult) -> None:
        """Emit WorkflowSelected telemetry event."""
        event = Event(
            event_type=WORKFLOW_SELECTED,
            source="intent_resolver",
            data={
                "workflow_id": result.workflow_id,
                "matched_intent": result.matched_intent,
                "confidence": result.confidence,
            },
        )
        event_bus.publish(event)

    def _emit_execution_started(
        self,
        result: CatalogResolveResult,
        input_data: dict[str, Any] | None = None,
    ) -> None:
        """Emit WorkflowExecutionStarted telemetry event."""
        event = Event(
            event_type=WORKFLOW_EXECUTION_STARTED,
            source="intent_resolver",
            data={
                "workflow_id": result.workflow_id,
                "matched_intent": result.matched_intent,
                "has_input_data": input_data is not None,
            },
        )
        event_bus.publish(event)

    # ─── Utility ───

    def get_catalog(self) -> WorkflowCatalog:
        """Get the underlying catalog instance."""
        return self._catalog

    def get_registered_intents(self) -> list[str]:
        """Get all registered intents from the catalog."""
        return list(self._catalog.list_intents().keys())

    def get_registered_workflows(self) -> list[dict[str, Any]]:
        """Get all registered workflows from the catalog."""
        return self._catalog.list_entries()

    def clear(self) -> None:
        """Clear all resolver state (aliases, task names, catalog entries)."""
        self._aliases.clear()
        self._task_name_index.clear()
        self._catalog.clear()
        logger.info("IntentResolver cleared")


# ─── Singleton ───

intent_resolver = IntentResolver()

