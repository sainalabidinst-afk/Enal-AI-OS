"""
Document Processing Capability Pack — Core Engine module.

Provides the DocumentEngine: a pipeline-core that orchestrates
read → transform → write operations for DOCX/XLSX/PPTX/PDF documents.

Delegates file I/O to specialized sub-modules:
    - office_reader.py  (DOCX/XLSX/PPTX parsing)
    - pdf_reader.py     (PDF parsing)
    - office_writer.py  (DOCX/XLSX/PPTX generation & editing)
    - pdf_writer.py     (PDF generation, merge, split, annotate)

All optional dependencies (python-docx, openpyxl, python-pptx, PyPDF2/pypdf,
reportlab) are imported lazily via _lazy_import to maintain registry
loadability without hard dependencies.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Any

from apps.document_processing.office_reader import OfficeReader
from apps.document_processing.pdf_reader import PDFReader
from apps.document_processing.pdf_writer import PDFWriter
from apps.document_processing.schemas import (
    BatchJobResult,
    BatchSummary,
    ConvertedFile,
    DocumentContent,
    DocumentEditResult,
    DocumentFormat,
    DocumentMetadata,
    DocumentOperation,
    DocumentProcessingInputs,
    ProducedFile,
)

logger = logging.getLogger(__name__)


def _lazy_import(module_name: str) -> Any:
    """Import an optional dependency lazily, raising a clear error if unavailable."""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(
            f"Optional dependency '{module_name}' is required for this operation. "
            f"Install with: pip install {module_name.replace('-', '_')}"
        ) from e


class DocumentEngine:
    """
    Core document processing engine implementing the pipeline:
        read → transform → write

    Supports DOCX (python-docx), XLSX (openpyxl), PPTX (python-pptx),
    and PDF (PyPDF2 / pypdf, reportlab) formats with lazy-loaded optional
    dependencies.

    All operations use explicit inputs and disclose their formulae;
    no silent defaults are applied for missing values.
    """

    SUPPORTED_READ_FORMATS: set[str] = {"docx", "xlsx", "pptx", "pdf"}
    SUPPORTED_WRITE_FORMATS: set[str] = {"docx", "xlsx", "pptx", "pdf", "csv"}
    SUPPORTED_CONVERT_FORMATS: dict[str, set[str]] = {
        "docx": {"pdf"},
        "pptx": {"pdf"},
        "xlsx": {"csv"},
    }

    def __init__(self) -> None:
        self.office_reader = OfficeReader()
        self.pdf_reader = PDFReader()
        self.office_writer = None
        self.pdf_writer = None

    def _get_office_writer(self) -> Any:
        if self.office_writer is None:
            from apps.document_processing.office_writer import OfficeWriter
            self.office_writer = OfficeWriter()
        return self.office_writer

    def _get_pdf_writer(self) -> Any:
        if self.pdf_writer is None:
            self.pdf_writer = PDFWriter()
        return self.pdf_writer

    def check_input_validation(self, inputs: DocumentProcessingInputs) -> dict[str, Any]:
        """Validate inputs for missing or ambiguous values."""
        errors: list[str] = []
        valid = True

        if inputs.operation == DocumentOperation.document_read:
            if not inputs.source_path:
                errors.append("source_path is required for document_read")
                valid = False
            if not inputs.source_format:
                errors.append("source_format is required for document_read")
                valid = False
            elif inputs.source_format not in self.SUPPORTED_READ_FORMATS:
                errors.append(
                    f"source_format '{inputs.source_format}' not supported for reading. "
                    f"Supported: {sorted(self.SUPPORTED_READ_FORMATS)}"
                )
                valid = False

        if inputs.operation == DocumentOperation.document_edit:
            if not inputs.source_path:
                errors.append("source_path is required for document_edit")
                valid = False
            if not inputs.text_replacements and not inputs.table_operations \
                    and not inputs.metadata:
                errors.append(
                    "At least one of text_replacements, table_operations, or metadata "
                    "is required for document_edit"
                )
                valid = False

        if inputs.operation == DocumentOperation.document_produce:
            if not inputs.produce_content:
                errors.append("produce_content is required for document_produce")
                valid = False
            if not inputs.output_path:
                errors.append("output_path is required for document_produce")
                valid = False

        if inputs.operation == DocumentOperation.document_convert:
            if not inputs.source_path:
                errors.append("source_path is required for document_convert")
                valid = False
            if not inputs.target_format:
                errors.append("target_format is required for document_convert")
                valid = False

        if inputs.operation == DocumentOperation.document_annotate:
            if not inputs.source_path:
                errors.append("source_path is required for document_annotate")
                valid = False
            if not inputs.annotations:
                errors.append("annotations is required for document_annotate")
                valid = False

        if inputs.operation == DocumentOperation.batch_process:
            if not inputs.batch_jobs:
                errors.append("batch_jobs is required for batch_process")
                valid = False

        return {
            "valid": valid and len(errors) == 0,
            "validation_errors": errors,
            "calculation_performed": valid,
        }

    # ------------------------------------------------------------------
    # Document Read — delegates to OfficeReader / PDFReader
    # ------------------------------------------------------------------

    def read_document(self, inputs: DocumentProcessingInputs) -> DocumentContent:
        """Read and parse a document file, returning structured content."""
        source_path = inputs.source_path or ""
        source_format = inputs.source_format or ""

        if not source_path or not os.path.exists(source_path):
            return DocumentContent(
                format=DocumentFormat(source_format) if source_format in DocumentFormat.__members__
                else DocumentFormat.docx,
                text="",
                metadata=DocumentMetadata(),
                formula="none",
                inputs_traced=["source_path"],
                word_count=0,
            )

        fmt = DocumentFormat(source_format)

        if fmt in (DocumentFormat.docx, DocumentFormat.xlsx, DocumentFormat.pptx):
            content = self.office_reader.read(source_path, fmt.value)
            if content is not None:
                return content

        if fmt == DocumentFormat.pdf:
            return self.pdf_reader.read(source_path)

        return DocumentContent(
            format=fmt,
            text="",
            formula="unsupported format",
            inputs_traced=["source_path", "source_format"],
        )

    # ------------------------------------------------------------------
    # Document Edit — delegates to OfficeWriter
    # ------------------------------------------------------------------

    def edit_document(self, inputs: DocumentProcessingInputs) -> list[DocumentEditResult]:
        """Edit a document: text replacement, table modification, metadata update."""
        source_path = inputs.source_path or ""

        if not source_path or not os.path.exists(source_path):
            return [DocumentEditResult(
                target=source_path,
                status="failed",
                details="Source file does not exist",
            )]

        writer = self._get_office_writer()
        return writer.edit(source_path, inputs)

    # ------------------------------------------------------------------
    # Document Produce — delegates to OfficeWriter / PDFWriter
    # ------------------------------------------------------------------

    def produce_document(self, inputs: DocumentProcessingInputs) -> list[ProducedFile]:
        """Generate a new document file from a content model."""
        output_path = inputs.output_path or ""
        content = inputs.produce_content

        if not content or not output_path:
            return []

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        doc_type = content.document_type

        if doc_type == "pdf":
            self._get_pdf_writer().produce_pdf(output_path, content)
        elif doc_type in ("word", "excel", "powerpoint"):
            self._get_office_writer().produce(output_path, content)
        else:
            return []

        produced: list[ProducedFile] = []
        if os.path.exists(output_path):
            produced.append(ProducedFile(
                path=output_path,
                format=doc_type,
                size_bytes=os.path.getsize(output_path),
                status="generated",
            ))

        return produced

    # ------------------------------------------------------------------
    # Document Convert — delegates to OfficeWriter / PDFWriter
    # ------------------------------------------------------------------

    def convert_document(self, inputs: DocumentProcessingInputs) -> list[ConvertedFile]:
        """Convert a document from one format to another."""
        source_path = inputs.source_path or ""
        target_format = inputs.target_format or ""

        if not source_path or not os.path.exists(source_path) or not target_format:
            return []

        results: list[ConvertedFile] = []
        source_ext = os.path.splitext(source_path)[1].lower().lstrip(".")

        base_name = os.path.splitext(os.path.basename(source_path))[0]
        output_dir = os.path.dirname(source_path) or "."
        output_path = os.path.join(output_dir, f"{base_name}.{target_format}")

        supported_targets = self.SUPPORTED_CONVERT_FORMATS.get(source_ext, set())
        if target_format not in supported_targets:
            results.append(ConvertedFile(
                source=source_path,
                output=output_path,
                format=target_format,
                status="failed",
            ))
            return results

        pw = self._get_pdf_writer()
        success = False
        if source_ext == "docx" and target_format == "pdf":
            success = pw.convert_docx_to_pdf(source_path, output_path)
        elif source_ext == "pptx" and target_format == "pdf":
            success = pw.convert_pptx_to_pdf(source_path, output_path)
        elif source_ext == "xlsx" and target_format == "csv":
            success = pw.convert_xlsx_to_csv(source_path, output_path)

        status = "success" if success and os.path.exists(output_path) else "failed"
        results.append(ConvertedFile(
            source=source_path,
            output=output_path,
            format=target_format,
            status=status,
        ))
        return results

    # ------------------------------------------------------------------
    # Document Annotate — delegates to OfficeWriter / PDFWriter
    # ------------------------------------------------------------------

    def annotate_document(
        self, inputs: DocumentProcessingInputs
    ) -> list[Any]:
        """Add annotations (comments, highlights, watermarks) to a document."""
        source_path = inputs.source_path or ""

        if not source_path or not os.path.exists(source_path):
            return []

        ext = os.path.splitext(source_path)[1].lower().lstrip(".")
        results: list[Any] = []

        if ext == "docx":
            results = self._get_office_writer().annotate_docx(source_path, inputs.annotations)
        elif ext == "pdf":
            results = self._get_pdf_writer().annotate_pdf(source_path, inputs.annotations)

        return results

    # ------------------------------------------------------------------
    # Batch Processing
    # ------------------------------------------------------------------

    def run_batch(self, inputs: DocumentProcessingInputs) -> BatchSummary:
        """Process multiple document jobs with configurable parallelism."""
        jobs = inputs.batch_jobs
        results: list[BatchJobResult] = []
        succeeded = 0
        failed = 0

        for job in jobs:
            job_id = job.get("id", f"batch-job-{len(results)}")
            op_str = job.get("operation", "")
            try:
                op = DocumentOperation(op_str)
            except ValueError:
                op = DocumentOperation.document_read

            job_inputs = DocumentProcessingInputs(
                operation=op,
                source_path=job.get("source_path"),
                source_format=job.get("source_format"),
                target_format=job.get("target_format"),
                output_path=job.get("output_path"),
                text_replacements=job.get("text_replacements", []),
                table_operations=job.get("table_operations", []),
                metadata=job.get("metadata", {}),
                annotations=job.get("annotations", []),
                produce_content=job.get("produce_content"),
                source_id=job.get("source_id"),
            )

            try:
                if op == DocumentOperation.document_read:
                    self.read_document(job_inputs)
                elif op == DocumentOperation.document_edit:
                    self.edit_document(job_inputs)
                elif op == DocumentOperation.document_convert:
                    self.convert_document(job_inputs)
                elif op == DocumentOperation.document_produce:
                    self.produce_document(job_inputs)
                elif op == DocumentOperation.document_annotate:
                    self.annotate_document(job_inputs)
                else:
                    raise ValueError(f"Unknown operation: {op_str}")

                results.append(BatchJobResult(
                    job_id=job_id,
                    operation=op_str,
                    status="success",
                    output=job.get("target_path") or job.get("output_path"),
                ))
                succeeded += 1
            except ImportError as e:
                results.append(BatchJobResult(
                    job_id=job_id,
                    operation=op_str,
                    status="failed",
                    error=f"Dependency not installed: {e}",
                ))
                failed += 1
            except Exception as e:
                results.append(BatchJobResult(
                    job_id=job_id,
                    operation=op_str,
                    status="failed",
                    error=str(e),
                ))
                failed += 1

        return BatchSummary(
            total=len(jobs),
            succeeded=succeeded,
            failed=failed,
            results=results,
        )


__all__ = ["DocumentEngine", "_lazy_import"]
