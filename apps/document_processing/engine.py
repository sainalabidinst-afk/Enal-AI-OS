"""
Document Processing Capability Pack — Engine.

Orchestrates the document processing pipeline:
    read → transform → write

Delegates to DocumentEngine for the core pipeline and produces
DocumentProcessingReport with formula disclosure, input lineage,
and safety boundary enforcement.
"""

from __future__ import annotations

import logging

from apps.document_processing.document_engine import DocumentEngine
from apps.document_processing.schemas import (
    BatchSummary,
    BusinessContext,
    ConvertedFile,
    DocumentContent,
    DocumentEditResult,
    DocumentOperation,
    DocumentProcessingInputs,
    DocumentProcessingReport,
    DocumentProcessingRequest,
    ProducedFile,
)

logger = logging.getLogger(__name__)


class DocumentProcessingEngine:
    """
    Orchestrates the document processing pipeline:
        1. Document Read (parsing DOCX/XLSX/PPTX/PDF)
        2. Document Edit (text, tables, metadata)
        3. Document Produce (generasi file baru)
        4. Document Convert (Word→PDF, PPTX→PDF, Excel→CSV)
        5. Document Annotate (komentar, highlight, watermark)
        6. Batch Processing (paralel dokumen)
    """

    VERSION = "1.0.0"

    def __init__(self) -> None:
        self.engine = DocumentEngine()

    def execute(self, request: DocumentProcessingRequest) -> DocumentProcessingReport:
        inputs: DocumentProcessingInputs = request.inputs
        ctx: BusinessContext = request.business_context
        validation = self.engine.check_input_validation(inputs)

        limitations = [
            "Document processing outputs are descriptive; validate results before publication",
            "Text-based PDF conversion may not preserve complex layouts",
            "Optional dependencies (python-docx, openpyxl, python-pptx, reportlab) "
            "must be installed for active operations",
            "OCR is not supported — scanned PDFs require external preprocessing",
        ]
        recommendations = [
            "Verify output files in target application before finalizing",
            "Review parsed content against source for accuracy",
            "Keep optional dependencies updated for best format compatibility",
            "Use batch processing for throughput on multiple documents",
        ]
        assumptions = [f"document processing for {ctx.project_name}"]

        document_content: DocumentContent | None = None
        edit_results: list[DocumentEditResult] = []
        produced_files: list[ProducedFile] = []
        converted_files: list[ConvertedFile] = []
        annotated_files = []
        batch_summary: BatchSummary | None = None

        source_reference_preserved = inputs.source_id is not None

        if not validation["valid"]:
            limitations.append(f"Input validation failed: {validation['validation_errors']}")

        if inputs.operation == DocumentOperation.document_read:
            document_content = self.engine.read_document(inputs)
            assumptions.append(f"source_format={inputs.source_format}")

        if inputs.operation == DocumentOperation.document_edit:
            edit_results = self.engine.edit_document(inputs)
            assumptions.append(
                f"edit operations: {len(inputs.text_replacements)} replacements, "
                f"{len(inputs.table_operations)} table ops, "
                f"{len(inputs.metadata)} metadata keys"
            )

        if inputs.operation == DocumentOperation.document_produce:
            produced_files = self.engine.produce_document(inputs)
            doc_type = inputs.produce_content.document_type if inputs.produce_content else "none"
            assumptions.append(f"produce_content document_type={doc_type}")

        if inputs.operation == DocumentOperation.document_convert:
            converted_files = self.engine.convert_document(inputs)
            assumptions.append(f"convert: {inputs.source_format} → {inputs.target_format}")

        if inputs.operation == DocumentOperation.document_annotate:
            annotated_files = self.engine.annotate_document(inputs)
            assumptions.append(f"annotations: {len(inputs.annotations)}")

        if inputs.operation == DocumentOperation.batch_process:
            batch_summary = self.engine.run_batch(inputs)
            assumptions.append(
                f"batch jobs: {len(inputs.batch_jobs)}, parallelism={inputs.parallelism}"
            )

        quality_score = 0.92 if validation["valid"] else 0.80

        formula = self._formula_for(inputs.operation, validation)

        inputs_traced = self._trace_inputs(inputs, validation)

        return DocumentProcessingReport(
            request_id=request.request_id,
            operation=inputs.operation,
            document_content=document_content,
            edit_results=edit_results,
            produced_files=produced_files,
            converted_files=converted_files,
            annotated_files=annotated_files,
            batch_summary=batch_summary,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            source_reference_preserved=source_reference_preserved,
            formula=formula,
            inputs_traced=inputs_traced,
            model_version=self.VERSION,
            quality_score=quality_score,
        )

    def _formula_for(self, operation: DocumentOperation, validation: dict) -> str:
        formulas = {
            DocumentOperation.document_read: ("read: parse source file via lazy imported library"),
            DocumentOperation.document_edit: ("edit: text_replace + table_ops + metadata_update"),
            DocumentOperation.document_produce: (
                "produce: build from content model via lazy imported library"
            ),
            DocumentOperation.document_convert: (
                "convert: source_format -> target_format via writer pipeline"
            ),
            DocumentOperation.document_annotate: (
                "annotate: add comments/highlights/watermarks to source"
            ),
            DocumentOperation.batch_process: (
                "batch: iterate jobs, route per operation, summarize"
            ),
        }
        base = formulas.get(operation, "unknown")
        if not validation["valid"]:
            return f"{base} | input_validation_failed: {validation['validation_errors']}"
        return base

    def _trace_inputs(self, inputs: DocumentProcessingInputs, validation: dict) -> list[str]:
        traced: list[str] = []
        if inputs.source_path:
            traced.append("source_path")
        if inputs.source_format:
            traced.append("source_format")
        if inputs.text_replacements:
            traced.append("text_replacements")
        if inputs.table_operations:
            traced.append("table_operations")
        if inputs.metadata:
            traced.append("metadata")
        if inputs.target_format:
            traced.append("target_format")
        if inputs.output_path:
            traced.append("output_path")
        if inputs.annotations:
            traced.append("annotations")
        if inputs.produce_content:
            traced.append("produce_content")
        if inputs.batch_jobs:
            traced.append("batch_jobs")
        if inputs.source_id:
            traced.append(inputs.source_id)
        if inputs.checklist_version:
            traced.append("checklist_version")
        if not validation["valid"]:
            traced.append("validation_error")
        return traced

    def get_record(self) -> dict:
        """Return a capability record for registry/memory."""
        return {
            "pack_id": "document-processing",
            "version": self.VERSION,
            "capabilities": [
                "document_read",
                "document_edit",
                "document_produce",
                "document_convert",
                "document_annotate",
                "batch_process",
            ],
        }


__all__ = ["DocumentProcessingEngine"]
