from __future__ import annotations

from backend.app.core.knowledge.store import KnowledgeStore

from apps.trading_analyst.knowledge.seeders.trading import seed_trading_knowledge


def build_knowledge_store() -> KnowledgeStore:
    store = KnowledgeStore()
    seed_trading_knowledge(store.registry, store.graph)
    return store


knowledge_store = build_knowledge_store()
