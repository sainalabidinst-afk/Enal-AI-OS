"""
Workflow Catalog & Resolver
============================

Memetakan intent/task identifier ke workflow statis yang sudah ada.

Resolver tidak membuat workflow baru.
Resolver tidak melakukan reasoning.
Resolver hanya memilih workflow dari katalog berdasarkan
aturan yang telah didefinisikan.

Flow:
    Intent/Task Identifier
        |
    WorkflowResolver.resolve(intent)
        |
    +-- Jika cocok  -> WorkflowCatalogEntry
    +-- Jika tidak  -> ResolveError (standar)

Katalog dapat diisi:
    - Dari dictionary/JSON saat runtime
    - Dari file JSON
    - Langsung via API register()
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# --- Data classes ---


@dataclass
class WorkflowCatalogEntry:
    """An entry in the workflow catalog mapping intents to workflows.

    Attributes:
        workflow_id: The workflow to execute for matching intents.
        display_name: Human-readable name of this catalog entry.
        description: Description of what this entry does.
        supported_intents: List of intent/task identifiers that resolve to this workflow.
        tags: Optional tags for categorization.
        metadata: Additional metadata.
    """
    workflow_id: str
    display_name: str
    description: str = ""
    supported_intents: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResolveResult:
    """Standardized output from the resolver.

    Attributes:
        found: Whether a matching workflow was found.
        workflow_id: The matched workflow_id (None if not found).
        entry: The catalog entry (None if not found).
        error: Error message if not found (None on success).
        matched_intent: The specific intent that matched.
    """
    found: bool
    workflow_id: str | None
    entry: WorkflowCatalogEntry | None
    error: str | None = None
    matched_intent: str | None = None


# --- Error ---


class CatalogError(Exception):
    """Raised on catalog-level errors (validation, duplicates, I/O)."""


class ResolveError(ValueError):
    """Raised when no workflow matches the given intent.

    This is the standardized error for unmatched intents.
    """

    def __init__(self, intent: str, message: str | None = None) -> None:
        self.intent = intent
        self.message = message or f"No workflow found for intent: '{intent}'"
        super().__init__(self.message)


# --- Catalog ---


class WorkflowCatalog:
    """Catalog that maps intents/tasks to static workflow definitions.

    Catalog responsibilities:
        - Store entries mapping intents -> workflow_id
        - Detect duplicate intents at registration time
        - Provide lookup by intent
        - Support loading from dict, JSON, and file
        - List all registered intents and their mappings

    Catalog is NOT a planner.
    It simply stores static mappings.
    """

    def __init__(self) -> None:
        self._intent_index: dict[str, WorkflowCatalogEntry] = {}
        self._entries: dict[str, WorkflowCatalogEntry] = {}
        self._intent_to_entry_id: dict[str, str] = {}

    # --- Registration ---

    def register(self, entry: WorkflowCatalogEntry) -> None:
        """Register a catalog entry.

        Raises:
            CatalogError: If entry has no workflow_id or no supported_intents.
            CatalogError: If any intent is already registered (duplicate detection).
        """
        if not entry.workflow_id:
            raise CatalogError("workflow_id is required")
        if not entry.supported_intents:
            raise CatalogError(
                f"Entry '{entry.workflow_id}' must have at least one supported_intent"
            )

        for intent in entry.supported_intents:
            existing = self._intent_to_entry_id.get(intent)
            if existing is not None and existing != entry.workflow_id:
                raise CatalogError(
                    f"Duplicate intent '{intent}': already mapped to workflow '{existing}', "
                    f"cannot also map to '{entry.workflow_id}'"
                )

        self._entries[entry.workflow_id] = entry
        for intent in entry.supported_intents:
            self._intent_index[intent] = entry
            self._intent_to_entry_id[intent] = entry.workflow_id

        logger.info(
            "Catalog entry registered: %s (%s) with %d intents",
            entry.workflow_id,
            entry.display_name,
            len(entry.supported_intents),
        )

    def register_from_dict(self, data: dict[str, Any]) -> WorkflowCatalogEntry:
        """Register from a dictionary."""
        entry = WorkflowCatalogEntry(
            workflow_id=data["workflow_id"],
            display_name=data.get("display_name", data["workflow_id"]),
            description=data.get("description", ""),
            supported_intents=data.get("supported_intents", []),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
        )
        self.register(entry)
        return entry

    def register_from_json(self, json_str: str) -> WorkflowCatalogEntry:
        """Register from a JSON string."""
        data = json.loads(json_str)
        return self.register_from_dict(data)

    def register_from_file(self, filepath: str) -> WorkflowCatalogEntry:
        """Register from a JSON file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Catalog file not found: {filepath}")
        content = path.read_text(encoding="utf-8")
        return self.register_from_json(content)

    # --- Lookup / Resolution ---

    def resolve(self, intent: str) -> ResolveResult:
        """Resolve an intent to a workflow catalog entry.

        Args:
            intent: The intent/task identifier to resolve.

        Returns:
            ResolveResult with found=True and entry if matched,
            or found=False with a standardized error if not.
        """
        if not intent or not intent.strip():
            return ResolveResult(
                found=False,
                workflow_id=None,
                entry=None,
                error="Intent cannot be empty",
            )

        entry = self._intent_index.get(intent)
        if entry is None:
            return ResolveResult(
                found=False,
                workflow_id=None,
                entry=None,
                error=f"No workflow found for intent: '{intent}'",
                matched_intent=None,
            )

        return ResolveResult(
            found=True,
            workflow_id=entry.workflow_id,
            entry=entry,
            error=None,
            matched_intent=intent,
        )

    def resolve_or_raise(self, intent: str) -> WorkflowCatalogEntry:
        """Resolve an intent or raise ResolveError if not found."""
        result = self.resolve(intent)
        if not result.found:
            raise ResolveError(intent, result.error)
        return result.entry  # type: ignore[return-value]

    def get_entry(self, workflow_id: str) -> WorkflowCatalogEntry | None:
        """Get catalog entry by workflow_id."""
        return self._entries.get(workflow_id)

    def get_workflow_id(self, intent: str) -> str | None:
        """Quick lookup: get workflow_id for an intent (or None)."""
        entry = self._intent_index.get(intent)
        return entry.workflow_id if entry else None

    def find_by_tag(self, tag: str) -> list[WorkflowCatalogEntry]:
        """Find all entries with a specific tag."""
        return [e for e in self._entries.values() if tag in e.tags]

    def list_entries(self) -> list[dict[str, Any]]:
        """List all catalog entries (summary)."""
        return [
            {
                "workflow_id": e.workflow_id,
                "display_name": e.display_name,
                "description": e.description,
                "supported_intents": list(e.supported_intents),
                "tags": list(e.tags),
                "intent_count": len(e.supported_intents),
            }
            for e in self._entries.values()
        ]

    def list_intents(self) -> dict[str, str]:
        """List all registered intents and their mapped workflow_id."""
        return dict(self._intent_to_entry_id)

    def entry_count(self) -> int:
        """Number of registered entries."""
        return len(self._entries)

    def intent_count(self) -> int:
        """Number of registered intents."""
        return len(self._intent_index)

    def clear(self) -> None:
        """Clear all entries from the catalog."""
        self._intent_index.clear()
        self._entries.clear()
        self._intent_to_entry_id.clear()
        logger.info("Catalog cleared")


# --- Singleton ---

workflow_catalog = WorkflowCatalog()
