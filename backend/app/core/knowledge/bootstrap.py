from __future__ import annotations

from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.graph import KnowledgeGraph
from backend.app.core.knowledge.store import KnowledgeStore
from backend.app.core.knowledge.seeders.trading import seed_trading_knowledge


def build_knowledge_store() -> KnowledgeStore:
    store = KnowledgeStore()
    seed_trading_knowledge(store.registry, store.graph)
    return store


knowledge_store = build_knowledge_store()
