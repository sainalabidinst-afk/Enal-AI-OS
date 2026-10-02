"""
Runtime — Public service facade for Capability Packs.
=================================================================

This module re-exports the public kernel services that Capability Packs
are permitted to import. It enforces the architectural boundary defined
in docs/GOVERNANCE.md:

  - Apps → sdk, runtime  ✓ (allowed)
  - Apps → backend.app.core.<internal>  ✗ (forbidden)
  - Kernel → apps                       ✗ (forbidden)

Public services exposed:
  - settings          (configuration)
  - model_router      (LLM routing)
  - adaptive_runtime  (execution runtime)
  - memory_manager    (7-layer memory)
  - knowledge         (knowledge graph services)
  - sandbox           (sandboxed execution)
  - workspace_service (workspace operations)
"""

from __future__ import annotations

# Re-export public configuration
from typing import Any

# Re-export adaptive runtime (lazy — actual runtime is accessed via method)
from backend.app.core.adaptive_runtime import adaptive_runtime
from backend.app.core.config import settings

# Re-export experience (for bootstrap)
from backend.app.core.experience import ExperienceLearning, experience_learning

# Re-export knowledge graph services (lazy import to avoid circular deps)
from backend.app.core.knowledge import (
    EvidenceBuilder,
    EvidenceStore,
    KnowledgeEdge,
    KnowledgeGraph,
    KnowledgeNode,
    KnowledgeRegistry,
    KnowledgeRetrieval,
    KnowledgeStore,
)

# Re-export memory layer services
from backend.app.core.memory_layer import (
    ConversationMemory,
    EpisodicMemory,
    KnowledgeMemory,
    LongTermMemory,
    MemoryLayer,
    MemoryManager,
    ProjectMemory,
    SessionMemory,
    WorkingMemory,
    memory_manager,
)

# Re-export model routing
from backend.app.core.model_router import model_router

# Re-export sandbox
from backend.app.core.sandbox import (
    SandboxExecution,
    SandboxLanguage,
    SandboxRuntime,
    sandbox_runtime,
)
from backend.app.core.workspace_service import WorkspaceService

# Storage (MinIO), Kafka event bus, DNS service, and connectors are lazily
# loaded via __getattr__ to avoid hard dependencies on optional packages.
# Access them directly: from backend.app.runtime import storage  # noqa: F821


def __getattr__(name: str) -> Any:
    """Lazy-load optional infrastructure modules on first access."""
    _lazy = {
        "MinioStorage": ("backend.app.core.storage", "MinioStorage"),
        "StorageError": ("backend.app.core.storage", "StorageError"),
        "storage": ("backend.app.core.storage", "storage"),
        "KafkaEventBus": ("backend.app.core.kafka_event_bus", "KafkaEventBus"),
        "kafka_event_bus": ("backend.app.core.kafka_event_bus", "kafka_event_bus"),
        "DNSService": ("backend.app.core.dns_service", "DNSService"),
        "DNSServiceDiscovery": ("backend.app.core.dns_service", "DNSServiceDiscovery"),
        "DNSServiceError": ("backend.app.core.dns_service", "DNSError"),
        "dns_service": ("backend.app.core.dns_service", "dns_service"),
        "BaseConnector": ("backend.app.connectors", "BaseConnector"),
        "ConnectorError": ("backend.app.connectors", "ConnectorError"),
        "ConnectorManager": ("backend.app.connectors", "ConnectorManager"),
        "connector_manager": ("backend.app.connectors", "connector_manager"),
        "OrderRequest": ("backend.app.connectors", "OrderRequest"),
        "OrderResponse": ("backend.app.connectors", "OrderResponse"),
        "OrderSide": ("backend.app.connectors", "OrderSide"),
        "OrderStatus": ("backend.app.connectors", "OrderStatus"),
        "OrderType": ("backend.app.connectors", "OrderType"),
        "PaperTradingConnector": ("backend.app.connectors", "PaperTradingConnector"),
        "FIXConnector": ("backend.app.connectors.fix_connector", "FIXConnector"),
        "conversation_store": ("backend.app.core.memory", "conversation_store"),
    }
    if name in _lazy:
        import importlib
        mod_path, attr = _lazy[name]
        module = importlib.import_module(mod_path)
        value = getattr(module, attr)
        globals()[name] = value
        return value
    raise AttributeError(f"module 'backend.app.runtime' has no attribute '{name}'")


# App loader — allows kernel to dynamically access apps without direct imports
# This maintains the governance rule: kernel never imports from apps directly
def load_app_engine(app_module: str, class_name: str):
    """Dynamically load an app engine class without creating a hard import dependency.

    Args:
        app_module: e.g. 'apps.scenario_simulator.engine'
        class_name: e.g. 'ScenarioSimulatorEngine'

    Returns:
        The class object
    """
    import importlib
    module = importlib.import_module(app_module)
    return getattr(module, class_name)


__all__ = [
    "settings",
    "model_router",
    "adaptive_runtime",
    "MemoryManager",
    "MemoryLayer",
    "WorkingMemory",
    "ConversationMemory",
    "KnowledgeMemory",
    "LongTermMemory",
    "ProjectMemory",
    "SessionMemory",
    "EpisodicMemory",
    "memory_manager",
    "EvidenceStore",
    "EvidenceBuilder",
    "KnowledgeGraph",
    "KnowledgeNode",
    "KnowledgeEdge",
    "KnowledgeRegistry",
    "KnowledgeRetrieval",
    "KnowledgeStore",
    "SandboxExecution",
    "SandboxLanguage",
    "SandboxRuntime",
    "sandbox_runtime",
    "MinioStorage",
    "StorageError",
    "storage",
    "KafkaEventBus",
    "kafka_event_bus",
    "DNSService",
    "DNSServiceDiscovery",
    "DNSServiceError",
    "dns_service",
    "BaseConnector",
    "ConnectorError",
    "ConnectorManager",
    "connector_manager",
    "OrderRequest",
    "OrderResponse",
    "OrderSide",
    "OrderStatus",
    "OrderType",
    "PaperTradingConnector",
    "FIXConnector",
    "WorkspaceService",
    "ExperienceLearning",
    "experience_learning",
]
