"""
Document Processing Capability Pack — PDF Reader module.

Parses PDF files and returns structured DocumentContent.
Uses PyPDF2 or pypdf (lazy import).
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


class PDFReader:
    """Reads PDF files into structured content."""

    def read(self, path: str) -> DocumentContent:
        """Parse a PDF file and extract text, metadata, and page count."""
        if not os.path.exists(path):
            return DocumentContent(
                format=DocumentFormat.pdf,
                formula="file not found",
                inputs_traced=["source_path"],
            )

        pages_text: list[str] = []
        metadata = DocumentMetadata()
        page_count: int | None = None

        try:
            pypdf = _lazy_import("pypdf")
            reader = pypdf.PdfReader(path)
            page_count = len(reader.pages)
            for page in reader.pages:
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                pages_text.append(text.strip())

            if reader.metadata:
                metadata.author = reader.metadata.get("/Author")
                metadata.title = reader.metadata.get("/Title")
                metadata.subject = reader.metadata.get("/Subject")
                metadata.version = reader.metadata.get("/Version")
        except ImportError:
            pdf2 = _lazy_import("PyPDF2")
            reader = pdf2.PdfReader(path)
            page_count = len(reader.pages)
            for page in reader.pages:
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                pages_text.append(text.strip())

            if reader.metadata:
                metadata.author = reader.metadata.get("/Author")
                metadata.title = reader.metadata.get("/Title")
                metadata.subject = reader.metadata.get("/Subject")

        text = "\n".join(p for p in pages_text if p)

        return DocumentContent(
            format=DocumentFormat.pdf,
            text=text,
            metadata=metadata,
            page_count=page_count,
            word_count=len(text.split()) if text else 0,
            formula="pdf parse: pages + text + metadata via pypdf/PyPDF2",
            inputs_traced=["source_path"],
        )

    def get_page_count(self, path: str) -> int | None:
        """Return the number of pages in a PDF file."""
        if not os.path.exists(path):
            return None
        pypdf = _lazy_import("pypdf")
        reader = pypdf.PdfReader(path)
        return len(reader.pages)

    def extract_page_text(self, path: str, page_number: int) -> str:
        """Extract text from a specific page (0-indexed)."""
        if not os.path.exists(path):
            return ""
        pypdf = _lazy_import("pypdf")
        reader = pypdf.PdfReader(path)
        if page_number >= len(reader.pages):
            return ""
        return (reader.pages[page_number].extract_text() or "").strip()


__all__ = ["PDFReader"]
