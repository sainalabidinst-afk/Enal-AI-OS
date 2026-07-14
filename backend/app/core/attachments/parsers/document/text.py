from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
)
from backend.app.core.attachments.parsers.base import BaseParser


class PDFParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.filename.lower().endswith(".pdf")

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="pdf")
        ast.system["document_type"] = "pdf"
        ast.system["text_preview"] = content[:1000]
        return ast


class DOCXParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.filename.lower().endswith(".docx")

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="docx")
        ast.system["document_type"] = "docx"
        ast.system["text_preview"] = content[:1000]
        return ast


class ExcelParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.filename.lower().endswith((".xlsx", ".csv"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="excel")
        ast.system["document_type"] = "excel"
        ast.system["text_preview"] = content[:1000]
        return ast
