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
        "BaseActionConnector": ("backend.app.connectors.base_action", "BaseActionConnector"),
        "ActionConnectorManager": ("backend.app.connectors.base_action", "ActionConnectorManager"),
        "action_connector_manager": ("backend.app.connectors.base_action", "action_connector_manager"),
        "ActionResult": ("backend.app.connectors.base_action", "ActionResult"),
        "ActionRequest": ("backend.app.connectors.base_action", "ActionRequest"),
        "ActionType": ("backend.app.connectors.base_action", "ActionType"),
        "FileSystemConnector": ("backend.app.connectors.file_system", "FileSystemConnector"),
        "EmailConnector": ("backend.app.connectors.email", "EmailConnector"),
        "CalendarConnector": ("backend.app.connectors.calendar", "CalendarConnector"),
        "SmartHomeConnector": ("backend.app.connectors.smarthome", "SmartHomeConnector"),
        "safe_path": ("backend.app.connectors.base_action", "safe_path"),
        "conversation_store": ("backend.app.core.memory", "conversation_store"),
        # Lazy import plugin marketplace for glossary domain plugins
        "PluginManifest": ("backend.app.core.plugin_marketplace", "PluginManifest"),
        "PluginMarketplace": ("backend.app.core.plugin_marketplace", "PluginMarketplace"),
        "PluginStatus": ("backend.app.core.plugin_marketplace", "PluginStatus"),
        "plugin_marketplace": ("backend.app.core.plugin_marketplace", "plugin_marketplace"),
        # Lazy import observability for capability tracing
        "Observability": ("backend.app.core.observability", "Observability"),
        "SpanType": ("backend.app.core.observability", "SpanType"),
        "observability": ("backend.app.core.observability", "observability"),
        # Lazy import voice services (STT/TTS)
        "VoiceAgent": ("backend.app.core.voice_vision_agent", "VoiceAgent"),
        "VoiceTranscription": ("backend.app.core.voice_vision_agent", "VoiceTranscription"),
        "VisionAgent": ("backend.app.core.voice_vision_agent", "VisionAgent"),
        "VisionAnalysis": ("backend.app.core.voice_vision_agent", "VisionAnalysis"),
        "voice_agent": ("backend.app.core.voice_vision_agent", "voice_agent"),
        "vision_agent": ("backend.app.core.voice_vision_agent", "vision_agent"),
        "stt_service": ("backend.app.core.stt_service", "stt_service"),
        "STTService": ("backend.app.core.stt_service", "STTService"),
        "TranscriptionResult": ("backend.app.core.stt_service", "TranscriptionResult"),
        "tts_service": ("backend.app.core.tts_service", "tts_service"),
        "TTSService": ("backend.app.core.tts_service", "TTSService"),
        "SynthesisResult": ("backend.app.core.tts_service", "SynthesisResult"),
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
    "BaseActionConnector",
    "ActionConnectorManager",
    "action_connector_manager",
    "ActionResult",
    "ActionRequest",
    "ActionType",
    "FileSystemConnector",
    "EmailConnector",
    "CalendarConnector",
    "SmartHomeConnector",
    "safe_path",
    "WorkspaceService",
    "ExperienceLearning",
    "experience_learning",
    "PluginManifest",
    "PluginMarketplace",
    "PluginStatus",
    "plugin_marketplace",
    "Observability",
    "SpanType",
    "observability",
    "VoiceAgent",
    "VoiceTranscription",
    "VisionAgent",
    "VisionAnalysis",
    "voice_agent",
    "vision_agent",
    "stt_service",
    "STTService",
    "TranscriptionResult",
    "tts_service",
    "TTSService",
    "SynthesisResult",
]
