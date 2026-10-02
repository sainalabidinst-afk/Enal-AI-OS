"""
Document Processing Capability Pack — Office Writer module.

Generates new Office files (DOCX, XLSX, PPTX) and edits existing ones.
All optional dependencies are lazily imported.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Any

from apps.document_processing.schemas import (
    AnnotatedFile,
    AnnotationSpec,
    AnnotationType,
    DocumentEditResult,
    DocumentProcessingInputs,
    ProduceContent,
    ProducedFile,
)


def _lazy_import(module_name: str) -> Any:
    """Import an optional dependency lazily, raising a clear error if unavailable."""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(
            f"Optional dependency '{module_name}' is required for this operation. "
            f"Install with: pip install {module_name.replace('-', '_')}"
        ) from e


logger = logging.getLogger(__name__)


class OfficeWriter:
    """Writes and edits Office documents (DOCX, XLSX, PPTX)."""

    SUPPORTED_FORMATS: set[str] = {"docx", "xlsx", "pptx"}

    # ------------------------------------------------------------------
    # Edit operations
    # ------------------------------------------------------------------

    def edit(self, path: str, inputs: DocumentProcessingInputs) -> list[DocumentEditResult]:
        """Edit an Office document based on the provided operations."""
        results: list[DocumentEditResult] = []
        if not path or not os.path.exists(path):
            results.append(DocumentEditResult(
                target=path, status="failed", details="Source file does not exist"
            ))
            return results

        ext = os.path.splitext(path)[1].lower().lstrip(".")

        if ext == "docx":
            self._edit_docx(path, inputs, results)
        elif ext == "xlsx":
            self._edit_xlsx(path, inputs, results)
        elif ext == "pptx":
            self._edit_pptx(path, inputs, results)
        else:
            results.append(DocumentEditResult(
                target=path, status="failed",
                details=f"Editing not supported for format '{ext}'"
            ))

        return results

    def _edit_docx(
        self, path: str, inputs: DocumentProcessingInputs, results: list[DocumentEditResult]
    ) -> None:
        """Edit a DOCX file."""
        docx = _lazy_import("docx")
        doc = docx.Document(path)

        for replacement in inputs.text_replacements:
            count = 0
            for para in doc.paragraphs:
                if replacement.find in para.text:
                    para.text = para.text.replace(replacement.find, replacement.replace)
                    count += 1
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if replacement.find in cell.text:
                            cell.text = cell.text.replace(replacement.find, replacement.replace)
                            count += 1
            status = "success" if count > 0 else "partial"
            results.append(DocumentEditResult(
                target=f"text_replacement:{replacement.find}",
                status=status,
                details=f"Replaced '{replacement.find}' in {count} locations",
            ))

        for op in inputs.table_operations:
            try:
                table = doc.tables[0] if doc.tables else None
                if table and op.row < len(table.rows) \
                        and op.col < len(table.rows[op.row].cells):
                    table.rows[op.row].cells[op.col].text = op.value
                    results.append(DocumentEditResult(
                        target=f"table[{op.row}][{op.col}]", status="success",
                        details=f"Set cell value to '{op.value}'",
                    ))
                else:
                    results.append(DocumentEditResult(
                        target=f"table[{op.row}][{op.col}]", status="failed",
                        details=f"Table cell out of bounds (row={op.row}, col={op.col})",
                    ))
            except Exception as e:
                results.append(DocumentEditResult(
                    target=f"table[{op.row}][{op.col}]", status="failed",
                    details=str(e),
                ))

        for key, value in inputs.metadata.items():
            if hasattr(doc.core_properties, key):
                setattr(doc.core_properties, key, value)

        if inputs.metadata:
            results.append(DocumentEditResult(
                target="metadata", status="success",
                details=f"Updated metadata keys: {list(inputs.metadata.keys())}",
            ))

        doc.save(path)

    def _edit_xlsx(
        self, path: str, inputs: DocumentProcessingInputs, results: list[DocumentEditResult]
    ) -> None:
        """Edit an XLSX file."""
        openpyxl = _lazy_import("openpyxl")
        wb = openpyxl.load_workbook(path)
        ws = wb.active

        for replacement in inputs.text_replacements:
            count = 0
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is not None and replacement.find in str(cell.value):
                        cell.value = str(cell.value).replace(replacement.find, replacement.replace)
                        count += 1
            status = "success" if count > 0 else "partial"
            results.append(DocumentEditResult(
                target=f"text_replacement:{replacement.find}",
                status=status,
                details=f"Replaced '{replacement.find}' in {count} cells",
            ))

        for op in inputs.table_operations:
            try:
                cell = ws.cell(row=op.row + 1, column=op.col + 1)
                cell.value = op.value
                results.append(DocumentEditResult(
                    target=f"cell[{op.row}][{op.col}]", status="success",
                    details=f"Set cell value to '{op.value}'",
                ))
            except Exception as e:
                results.append(DocumentEditResult(
                    target=f"cell[{op.row}][{op.col}]", status="failed",
                    details=str(e),
                ))

        if inputs.metadata:
            props = wb.properties
            for key, value in inputs.metadata.items():
                if hasattr(props, key):
                    setattr(props, key, value)
            results.append(DocumentEditResult(
                target="metadata", status="success",
                details=f"Updated metadata keys: {list(inputs.metadata.keys())}",
            ))

        wb.save(path)

    def _edit_pptx(
        self, path: str, inputs: DocumentProcessingInputs, results: list[DocumentEditResult]
    ) -> None:
        """Edit a PPTX file."""
        pptx = _lazy_import("pptx")
        prs = pptx.Presentation(path)

        for replacement in inputs.text_replacements:
            count = 0
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text") and replacement.find in shape.text:
                        shape.text = shape.text.replace(replacement.find, replacement.replace)
                        count += 1
            status = "success" if count > 0 else "partial"
            results.append(DocumentEditResult(
                target=f"text_replacement:{replacement.find}",
                status=status,
                details=f"Replaced '{replacement.find}' in {count} shapes",
            ))

        if inputs.metadata:
            props = prs.core_properties
            for key, value in inputs.metadata.items():
                if hasattr(props, key):
                    setattr(props, key, value)
            results.append(DocumentEditResult(
                target="metadata", status="success",
                details=f"Updated metadata keys: {list(inputs.metadata.keys())}",
            ))

        prs.save(path)

    # ------------------------------------------------------------------
    # Produce operations
    # ------------------------------------------------------------------

    def produce(self, path: str, content: ProduceContent) -> list[ProducedFile]:
        """Generate a new Office document from a content model."""
        if not path or not content:
            return []

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        doc_type = content.document_type

        produced: list[ProducedFile] = []

        if doc_type == "word":
            self._produce_docx(path, content)
        elif doc_type == "excel":
            self._produce_xlsx(path, content)
        elif doc_type == "powerpoint":
            self._produce_pptx(path, content)
        else:
            return produced

        if os.path.exists(path):
            produced.append(ProducedFile(
                path=path,
                format=doc_type,
                size_bytes=os.path.getsize(path),
                status="generated",
            ))

        return produced

    def _produce_docx(self, path: str, content: ProduceContent) -> None:
        """Generate a DOCX file."""
        docx = _lazy_import("docx")
        doc = docx.Document()

        for section in content.sections:
            if section.title:
                doc.add_heading(section.title, level=1)
            for para in section.paragraphs:
                doc.add_paragraph(para)
            if section.tables:
                for table_data in section.tables:
                    rows = len(table_data) if table_data else 0
                    cols = len(table_data[0]) if rows > 0 and table_data[0] else 0
                    table = doc.add_table(rows=rows, cols=cols)
                    for r_idx, row_data in enumerate(table_data):
                        for c_idx, cell_val in enumerate(row_data):
                            if r_idx < len(table.rows) \
                                    and c_idx < len(table.rows[r_idx].cells):
                                table.rows[r_idx].cells[c_idx].text = cell_val

        doc.save(path)

    def _produce_xlsx(self, path: str, content: ProduceContent) -> None:
        """Generate an XLSX file."""
        openpyxl = _lazy_import("openpyxl")
        wb = openpyxl.Workbook()
        ws = wb.active

        row_idx = 1
        for section in content.sections:
            if section.title:
                ws.cell(row=row_idx, column=1, value=section.title)
                row_idx += 1
            for para in section.paragraphs:
                ws.cell(row=row_idx, column=1, value=para)
                row_idx += 1
            if section.tables:
                for table_data in section.tables:
                    for table_row in table_data:
                        for c_idx, cell_val in enumerate(table_row):
                            ws.cell(row=row_idx, column=c_idx + 1, value=cell_val)
                        row_idx += 1

        wb.save(path)

    def _produce_pptx(self, path: str, content: ProduceContent) -> None:
        """Generate a PPTX file."""
        pptx = _lazy_import("pptx")
        prs = pptx.Presentation()
        bullet_slide_layout = prs.slide_layouts[1]

        for section in content.sections:
            slide = prs.slides.add_slide(bullet_slide_layout)
            if section.title:
                title = slide.shapes.title
                if title:
                    title.text = section.title
            body_parts: list[str] = list(section.paragraphs)
            if len(slide.placeholders) > 1:
                slide.placeholders[1].text = "\n".join(body_parts)

        prs.save(path)

    def annotate_docx(
        self, path: str, annotations: list[AnnotationSpec]
    ) -> list[Any]:
        """Annotate a DOCX file with comments, highlights, and watermarks."""
        docx = _lazy_import("docx")
        doc = docx.Document(path)

        annotation_count = 0
        for ann in annotations:
            if ann.type == AnnotationType.comment:
                doc.add_paragraph(f"[KOMENTAR] {ann.content}", style="Intense Quote")
                annotation_count += 1
            elif ann.type == AnnotationType.highlight:
                doc.add_paragraph(f"[HIGHLIGHT] {ann.content}", style="Strong")
                annotation_count += 1
            elif ann.type == AnnotationType.watermark:
                if doc.sections:
                    header = doc.sections[0].header
                    paragraph = (
                        header.paragraphs[0]
                        if header.paragraphs
                        else header.add_paragraph()
                    )
                    paragraph.text = ann.content
                    annotation_count += 1

        doc.save(path)

        return [AnnotatedFile(
            path=path,
            annotation_count=annotation_count,
            status="success",
        )]

    def add_sheet(self, path: str, sheet_name: str, rows: list[list[Any]]) -> bool:
        """Add a new worksheet to an existing XLSX file."""
        openpyxl = _lazy_import("openpyxl")
        wb = openpyxl.load_workbook(path)
        if sheet_name in wb.sheetnames:
            return False
        ws = wb.create_sheet(sheet_name)
        for r_idx, row_data in enumerate(rows):
            for c_idx, cell_val in enumerate(row_data):
                ws.cell(row=r_idx + 1, column=c_idx + 1, value=cell_val)
        wb.save(path)
        return True


__all__ = ["OfficeWriter"]
