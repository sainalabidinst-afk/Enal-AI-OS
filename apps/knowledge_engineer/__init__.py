"""
Knowledge Engineer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.knowledge_engineer.engine import KnowledgeEngineerEngine
from apps.knowledge_engineer.schemas import (
    BusinessContext,
    EntityMapping,
    KnowledgeConfig,
    KnowledgeEngineerRecord,
    KnowledgeEngineerReport,
    KnowledgeEngineerRequest,
    KnowledgeOperation,
    KnowledgeStoreType,
    OntologyClass,
    RelationshipType,
)
from apps.knowledge_engineer.worker import KnowledgeEngineerWorker


class KnowledgeEngineerApp(BaseReferenceApp):
    name = "knowledge-engineer"
    version = "1.0.0"
    description = "Ontology design, knowledge graphs, entity resolution, and semantic search"
    category = "knowledge"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = KnowledgeEngineerWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> "KnowledgeEngineerApp":
    return KnowledgeEngineerApp()


__all__ = [
    "KnowledgeEngineerApp",
    "get_app",
    "KnowledgeEngineerEngine",
    "KnowledgeEngineerWorker",
    "KnowledgeEngineerRequest",
    "KnowledgeEngineerReport",
    "KnowledgeOperation",
    "KnowledgeStoreType",
    "OntologyClass",
    "RelationshipType",
    "EntityMapping",
    "KnowledgeConfig",
    "BusinessContext",
    "KnowledgeEngineerRecord",
]
