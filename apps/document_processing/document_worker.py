"""
Document Processing Capability Pack — Worker.

Thin adapter that exposes the DocumentProcessingEngine to the Execution Runtime
and agents. Converts dict-based task input to a typed DocumentProcessingRequest,
executes the engine, and returns a JSON-serializable dict.
"""

from __future__ import annotations

import json
from typing import Any

from apps.document_processing.engine import DocumentProcessingEngine
from apps.document_processing.schemas import DocumentProcessingRequest


class DocumentWorker:
    """Thin adapter that exposes the Document Processing engine to agents."""

    def __init__(self) -> None:
        self.engine = DocumentProcessingEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = DocumentProcessingRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["DocumentWorker"]
