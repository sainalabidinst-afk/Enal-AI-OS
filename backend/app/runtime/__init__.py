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
from backend.app.core.config import settings

# Re-export model routing
from backend.app.core.model_router import model_router

# Re-export adaptive runtime (lazy — actual runtime is accessed via method)
from backend.app.core.adaptive_runtime import adaptive_runtime

# Re-export memory layer services
from backend.app.core.memory_layer import (
    MemoryManager,
    MemoryLayer,
    WorkingMemory,
    ConversationMemory,
    KnowledgeMemory,
    LongTermMemory,
    ProjectMemory,
    SessionMemory,
    EpisodicMemory,
    memory_manager,
)

# Re-export knowledge graph services (lazy import to avoid circular deps)
from backend.app.core.knowledge import (
    EvidenceStore,
    EvidenceBuilder,
    KnowledgeGraph,
    KnowledgeNode,
    KnowledgeEdge,
    KnowledgeRegistry,
    KnowledgeRetrieval,
    KnowledgeStore,
)

# Re-export sandbox
from backend.app.core.sandbox import SandboxExecution, SandboxLanguage, SandboxRuntime, sandbox_runtime

# Re-export workspace service
from backend.app.core.workspace_service import WorkspaceService

# Re-export experience (for bootstrap)
from backend.app.core.experience import ExperienceLearning, experience_learning

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
    "SandboxExecutor",
    "WorkspaceService",
    "ExperienceTracker",
]
