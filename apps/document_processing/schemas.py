"""
Document Processing Capability Pack — Schemas
=============================================

Typed contracts for the Document Processing capability pack.
Defines input (DocumentProcessingRequest) and output (DocumentProcessingReport)
contracts for reading, editing, producing, converting, and annotating
DOCX/XLSX/PPTX/PDF documents.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class DocumentFormat(StrEnum):
    docx = "docx"
    xlsx = "xlsx"
    pptx = "pptx"
    pdf = "pdf"
    csv = "csv"


class DocumentOperation(StrEnum):
    document_read = "document_read"
    document_edit = "document_edit"
    document_produce = "document_produce"
    document_convert = "document_convert"
    document_annotate = "document_annotate"
    batch_process = "batch_process"


class AnnotationType(StrEnum):
    comment = "comment"
    highlight = "highlight"
    watermark = "watermark"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)


class TextReplacement(BaseModel):
    find: str
    replace: str


class TableOperation(BaseModel):
    row: int = Field(ge=0)
    col: int = Field(ge=0)
    value: str


class AnnotationSpec(BaseModel):
    type: AnnotationType
    content: str
    page: int | None = None
    coordinates: tuple[float, float, float, float] | None = None


class DocumentSection(BaseModel):
    title: str = ""
    paragraphs: list[str] = Field(default_factory=list)
    tables: list[list[str]] = Field(default_factory=list)


class DocumentMetadata(BaseModel):
    author: str | None = None
    title: str | None = None
    subject: str | None = None
    version: str | None = None
    created: str | None = None
    modified: str | None = None


class DocumentContent(BaseModel):
    format: DocumentFormat
    text: str = ""
    tables: list[list[list[str]]] = Field(default_factory=list)
    slides: list[str] = Field(default_factory=list)
    sheet_names: list[str] = Field(default_factory=list)
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    page_count: int | None = None
    word_count: int | None = None
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)


class ProduceSection(BaseModel):
    title: str = ""
    paragraphs: list[str] = Field(default_factory=list)
    tables: list[list[str]] = Field(default_factory=list)


class ProduceContent(BaseModel):
    document_type: str = "word"
    sections: list[ProduceSection] = Field(default_factory=list)


class DocumentProcessingInputs(BaseModel):
    operation: DocumentOperation
    # document_read
    source_path: str | None = None
    source_format: str | None = None
    # document_edit
    text_replacements: list[TextReplacement] = Field(default_factory=list)
    table_operations: list[TableOperation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    # document_produce
    produce_content: ProduceContent | None = None
    output_path: str | None = None
    # document_convert
    target_format: str | None = None
    # document_annotate
    annotations: list[AnnotationSpec] = Field(default_factory=list)
    # batch_process
    batch_jobs: list[dict[str, Any]] = Field(default_factory=list)
    parallelism: int = Field(default=4, ge=1, le=16)
    # common
    source_id: str | None = None
    checklist_version: str = "v1"
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class DocumentEditResult(BaseModel):
    target: str
    status: str = "success"
    details: str = ""


class ProducedFile(BaseModel):
    path: str
    format: str
    size_bytes: int = 0
    status: str = "generated"


class ConvertedFile(BaseModel):
    source: str
    output: str
    format: str
    status: str = "success"


class AnnotatedFile(BaseModel):
    path: str
    annotation_count: int
    status: str = "success"


class BatchJobResult(BaseModel):
    job_id: str
    operation: str
    status: str = "success"
    output: str | None = None
    error: str | None = None


class BatchSummary(BaseModel):
    total: int
    succeeded: int
    failed: int
    results: list[BatchJobResult] = Field(default_factory=list)


class DocumentProcessingRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "document_read"
    business_context: BusinessContext
    inputs: DocumentProcessingInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class DocumentProcessingReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: str
    document_content: DocumentContent | None = None
    edit_results: list[DocumentEditResult] = Field(default_factory=list)
    produced_files: list[ProducedFile] = Field(default_factory=list)
    converted_files: list[ConvertedFile] = Field(default_factory=list)
    annotated_files: list[AnnotatedFile] = Field(default_factory=list)
    batch_summary: BatchSummary | None = None
    findings: list[dict[str, Any]] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    source_reference_preserved: bool = False
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)
    model_version: str = "1.0.0"
    quality_score: float = Field(default=0.90, ge=0, le=1)


class DocumentProcessingRecord(BaseModel):
    pack_id: str = "document-processing"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "document_read",
        "document_edit",
        "document_produce",
        "document_convert",
        "document_annotate",
        "batch_process",
    ])


__all__ = [
    "AnnotationSpec",
    "AnnotationType",
    "AnnotatedFile",
    "BatchJobResult",
    "BatchSummary",
    "BusinessContext",
    "ConvertedFile",
    "DocumentContent",
    "DocumentEditResult",
    "DocumentFormat",
    "DocumentMetadata",
    "DocumentOperation",
    "DocumentProcessingInputs",
    "DocumentProcessingRecord",
    "DocumentProcessingReport",
    "DocumentProcessingRequest",
    "DocumentSection",
    "ProduceContent",
    "ProduceSection",
    "ProducedFile",
    "TableOperation",
    "TextReplacement",
]
