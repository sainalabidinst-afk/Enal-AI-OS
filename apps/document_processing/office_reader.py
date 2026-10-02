"""
Document Processing Capability Pack — Office Reader module.

Parses DOCX/XLSX/PPTX files and returns structured DocumentContent.
All optional dependencies are lazily imported.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Any

from apps.document_processing.schemas import (
    DocumentContent,
    DocumentFormat,
    DocumentMetadata,
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


class OfficeReader:
    """Reads Office documents (DOCX, XLSX, PPTX) into structured content."""

    SUPPORTED_FORMATS: set[str] = {"docx", "xlsx", "pptx"}

    def read(self, path: str, fmt: str) -> DocumentContent | None:
        """Dispatch to the appropriate format reader."""
        if fmt == "docx":
            return self.read_docx(path)
        if fmt == "xlsx":
            return self.read_xlsx(path)
        if fmt == "pptx":
            return self.read_pptx(path)
        return None

    def read_docx(self, path: str) -> DocumentContent:
        """Parse a DOCX file using python-docx (lazy import)."""
        if not os.path.exists(path):
            return DocumentContent(
                format=DocumentFormat.docx,
                formula="file not found",
                inputs_traced=["source_path"],
            )

        docx = _lazy_import("docx")
        doc = docx.Document(path)

        paragraphs: list[str] = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)

        tables: list[list[list[str]]] = []
        for table in doc.tables:
            table_data: list[list[str]] = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            tables.append(table_data)

        text = "\n".join(paragraphs)
        metadata = DocumentMetadata(
            author=doc.core_properties.author,
            title=doc.core_properties.title,
            subject=doc.core_properties.subject,
            version=doc.core_properties.version,
            created=str(doc.core_properties.created) if doc.core_properties.created else None,
            modified=str(doc.core_properties.modified) if doc.core_properties.modified else None,
        )

        return DocumentContent(
            format=DocumentFormat.docx,
            text=text,
            tables=tables,
            metadata=metadata,
            word_count=len(text.split()) if text else 0,
            formula="docx parse: paragraphs + tables via python-docx",
            inputs_traced=["source_path"],
        )

    def read_xlsx(self, path: str) -> DocumentContent:
        """Parse an XLSX file using openpyxl (lazy import)."""
        if not os.path.exists(path):
            return DocumentContent(
                format=DocumentFormat.xlsx,
                formula="file not found",
                inputs_traced=["source_path"],
            )

        openpyxl = _lazy_import("openpyxl")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)

        sheet_names: list[str] = list(wb.sheetnames)
        all_text_parts: list[str] = []
        tables: list[list[list[str]]] = []

        for sheet_name in sheet_names:
            ws = wb[sheet_name]
            sheet_table: list[list[str]] = []
            for row in ws.iter_rows(values_only=True):
                row_data = [str(val) if val is not None else "" for val in row]
                sheet_table.append(row_data)
                all_text_parts.extend(row_data)
            if sheet_table:
                tables.append(sheet_table)

        wb.close()
        text = "\n".join(all_text_parts)

        metadata = DocumentMetadata()
        try:
            props = wb.properties
            if props:
                metadata.author = getattr(props, "creator", None) or None
                metadata.title = getattr(props, "title", None) or None
                metadata.subject = getattr(props, "subject", None) or None
                metadata.version = getattr(props, "version", None) or None
        except Exception:
            pass

        return DocumentContent(
            format=DocumentFormat.xlsx,
            text=text,
            tables=tables,
            sheet_names=sheet_names,
            metadata=metadata,
            word_count=len(text.split()) if text else 0,
            formula="xlsx parse: sheets + cells via openpyxl",
            inputs_traced=["source_path"],
        )

    def read_pptx(self, path: str) -> DocumentContent:
        """Parse a PPTX file using python-pptx (lazy import)."""
        if not os.path.exists(path):
            return DocumentContent(
                format=DocumentFormat.pptx,
                formula="file not found",
                inputs_traced=["source_path"],
            )

        pptx = _lazy_import("pptx")
        prs = pptx.Presentation(path)

        slides: list[str] = []
        all_text: list[str] = []
        tables: list[list[list[str]]] = []

        for slide in prs.slides:
            slide_parts: list[str] = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    slide_parts.append(shape.text.strip())
                    all_text.append(shape.text.strip())
                if hasattr(shape, "table"):
                    table_data: list[list[str]] = []
                    for row in shape.table.rows:
                        table_data.append([cell.text.strip() for cell in row.cells])
                    tables.append(table_data)
            if slide_parts:
                slides.append("\n".join(slide_parts))

        text = "\n".join(all_text)
        metadata = DocumentMetadata()

        return DocumentContent(
            format=DocumentFormat.pptx,
            text=text,
            tables=tables,
            slides=slides,
            metadata=metadata,
            page_count=len(prs.slides),
            word_count=len(text.split()) if text else 0,
            formula="pptx parse: slides + text + tables via python-pptx",
            inputs_traced=["source_path"],
        )


__all__ = ["OfficeReader"]
