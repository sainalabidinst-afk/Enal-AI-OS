"""
Document Processing Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.document_processing.document_worker import DocumentWorker
from apps.document_processing.engine import DocumentProcessingEngine
from apps.document_processing.schemas import (
    AnnotatedFile,
    AnnotationSpec,
    AnnotationType,
    BatchJobResult,
    BatchSummary,
    BusinessContext,
    ConvertedFile,
    DocumentContent,
    DocumentEditResult,
    DocumentFormat,
    DocumentMetadata,
    DocumentOperation,
    DocumentProcessingInputs,
    DocumentProcessingRecord,
    DocumentProcessingReport,
    DocumentProcessingRequest,
    ProduceContent,
    ProducedFile,
    ProduceSection,
    TableOperation,
    TextReplacement,
)


class DocumentProcessingApp(BaseReferenceApp):
    name = "document-processing"
    version = "1.0.0"
    description = (
        "Read, edit, produce, convert, and annotate DOCX/XLSX/PPTX/PDF documents "
        "with lazy-import optional dependencies"
    )
    category = "productivity"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DocumentWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> DocumentProcessingApp:
    return DocumentProcessingApp()


__all__ = [
    "DocumentProcessingApp",
    "get_app",
    "DocumentProcessingEngine",
    "DocumentWorker",
    "DocumentProcessingRequest",
    "DocumentProcessingReport",
    "DocumentProcessingInputs",
    "DocumentOperation",
    "DocumentFormat",
    "DocumentContent",
    "DocumentEditResult",
    "DocumentMetadata",
    "ProduceContent",
    "ProduceSection",
    "ProducedFile",
    "ConvertedFile",
    "AnnotatedFile",
    "AnnotationSpec",
    "AnnotationType",
    "BatchJobResult",
    "BatchSummary",
    "BusinessContext",
    "TableOperation",
    "TextReplacement",
    "DocumentProcessingRecord",
]
