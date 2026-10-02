"""
Knowledge Engineer Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.knowledge_engineer.engine import KnowledgeEngineerEngine
from apps.knowledge_engineer.schemas import KnowledgeEngineerRequest


class KnowledgeEngineerWorker:
    """Thin adapter that exposes the Knowledge Engineer engine to agents."""

    def __init__(self) -> None:
        self.engine = KnowledgeEngineerEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = KnowledgeEngineerRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["KnowledgeEngineerWorker"]
