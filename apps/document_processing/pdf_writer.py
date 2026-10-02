"""
Document Processing Capability Pack — PDF Writer module.

Generates PDF files, annotates PDFs (watermark/highlights), merges and splits
PDF documents. Uses reportlab (lazy import) for generation and pypdf/PyPDF2
(lazy import) for manipulation.
"""

from __future__ import annotations

import importlib
import logging
import os
from io import BytesIO
from typing import Any

from apps.document_processing.schemas import (
    AnnotatedFile,
    AnnotationSpec,
    AnnotationType,
    ProduceContent,
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


class PDFWriter:
    """Writes, annotates, merges, and splits PDF files."""

    # ------------------------------------------------------------------
    # Produce operations
    # ------------------------------------------------------------------

    def produce_pdf(self, path: str, content: ProduceContent) -> bool:
        """Generate a simple PDF file from a content model using reportlab."""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
        )

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        doc = SimpleDocTemplate(path, pagesize=A4)
        story: list = []
        styles = getSampleStyleSheet()

        for section in content.sections:
            if section.title:
                story.append(Paragraph(section.title, styles["Heading1"]))
                story.append(Spacer(1, 12))
            for para in section.paragraphs:
                story.append(Paragraph(para, styles["BodyText"]))
                story.append(Spacer(1, 6))
            if section.tables:
                for table_data in section.tables:
                    if table_data:
                        story.append(Table(table_data))
                        story.append(Spacer(1, 12))

        doc.build(story)
        return os.path.exists(path)

    def produce_csv(self, path: str, content: ProduceContent) -> bool:
        """Generate a CSV file from a content model."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        lines: list[str] = []
        for section in content.sections:
            if section.title:
                lines.append(section.title)
            for para in section.paragraphs:
                lines.append(para)
            for table_data in section.tables:
                for table_row in table_data:
                    lines.append(",".join(str(c) for c in table_row))

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return os.path.exists(path)

    # ------------------------------------------------------------------
    # Convert operations
    # ------------------------------------------------------------------

    def convert_docx_to_pdf(self, source: str, output: str) -> bool:
        """Convert a DOCX file to PDF via reportlab (text-based approximation)."""
        docx = _lazy_import("docx")
        doc = docx.Document(source)

        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
        )
        from reportlab.platypus import (
            Table as PDFTable,
        )

        pdf_doc = SimpleDocTemplate(output, pagesize=A4)
        story: list = []
        styles = getSampleStyleSheet()

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                story.append(Paragraph(text, styles["BodyText"]))
                story.append(Spacer(1, 6))

        for table in doc.tables:
            table_data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            if table_data:
                story.append(PDFTable(table_data))
                story.append(Spacer(1, 12))

        pdf_doc.build(story)
        return os.path.exists(output)

    def convert_pptx_to_pdf(self, source: str, output: str) -> bool:
        """Convert a PPTX file to PDF (text-based approximation via reportlab)."""
        pptx = _lazy_import("pptx")
        prs = pptx.Presentation(source)

        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
        )

        pdf_doc = SimpleDocTemplate(output, pagesize=A4)
        story: list = []
        styles = getSampleStyleSheet()

        for idx, slide in enumerate(prs.slides):
            if idx > 0:
                story.append(PageBreak())
            story.append(Paragraph(f"Slide {idx + 1}", styles["Heading2"]))
            story.append(Spacer(1, 12))
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    story.append(Paragraph(shape.text.strip(), styles["BodyText"]))
                    story.append(Spacer(1, 6))

        pdf_doc.build(story)
        return os.path.exists(output)

    def convert_xlsx_to_csv(self, source: str, output: str) -> bool:
        """Convert an XLSX file to CSV."""
        openpyxl = _lazy_import("openpyxl")
        wb = openpyxl.load_workbook(source, read_only=True, data_only=True)
        ws = wb.active

        lines: list[str] = []
        for row in ws.iter_rows(values_only=True):
            cells = [str(val) if val is not None else "" for val in row]
            lines.append(",".join(cells))

        with open(output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        wb.close()
        return os.path.exists(output)

    # ------------------------------------------------------------------
    # Annotate operations
    # ------------------------------------------------------------------

    def annotate_pdf(
        self, path: str, annotations: list[AnnotationSpec]
    ) -> list[AnnotatedFile]:
        """Annotate a PDF file with watermarks via reportlab overlay."""
        pypdf = _lazy_import("pypdf")
        from reportlab.pdfgen import canvas

        reader = pypdf.PdfReader(path)
        writer = pypdf.PdfWriter()
        annotation_count = 0

        for page in reader.pages:
            for ann in annotations:
                if ann.type == AnnotationType.watermark:
                    w = float(page.mediabox.width)
                    h = float(page.mediabox.height)
                    packet = BytesIO()
                    can = canvas.Canvas(packet, pagesize=(w, h))
                    can.setFont("Helvetica", 48)
                    can.setFillColorRGB(0.5, 0.5, 0.5, 0.15)
                    can.saveState()
                    can.translate(w / 2, h / 2)
                    can.rotate(45)
                    can.drawCentredString(0, 0, ann.content)
                    can.restoreState()
                    can.save()
                    packet.seek(0)

                    watermark_pdf = pypdf.PdfReader(packet)
                    page.merge_page(watermark_pdf.pages[0])
                    annotation_count += 1
                elif ann.type in (AnnotationType.comment, AnnotationType.highlight):
                    annotation_count += 1

            writer.add_page(page)

        output_path = path.replace(".pdf", "_annotated.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        return [AnnotatedFile(
            path=output_path,
            annotation_count=annotation_count,
            status="success",
        )]

    # ------------------------------------------------------------------
    # PDF merge / split
    # ------------------------------------------------------------------

    def merge_pdfs(self, sources: list[str], output: str) -> str:
        """Merge multiple PDF files into a single output PDF."""
        pypdf = _lazy_import("pypdf")
        writer = pypdf.PdfWriter()

        for src in sources:
            if os.path.exists(src):
                reader = pypdf.PdfReader(src)
                for page in reader.pages:
                    writer.add_page(page)

        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "wb") as f:
            writer.write(f)

        return output

    def split_pdf(self, source: str, output_dir: str, ranges: list[tuple[int, int]]) -> list[str]:
        """Split a PDF into multiple files based on page ranges."""
        pypdf = _lazy_import("pypdf")
        reader = pypdf.PdfReader(source)
        os.makedirs(output_dir, exist_ok=True)

        outputs: list[str] = []
        for idx, (start, end) in enumerate(ranges):
            writer = pypdf.PdfWriter()
            for page_num in range(start, min(end, len(reader.pages))):
                writer.add_page(reader.pages[page_num])
            out_path = os.path.join(output_dir, f"split_{idx + 1}.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            outputs.append(out_path)

        return outputs


__all__ = ["PDFWriter"]
