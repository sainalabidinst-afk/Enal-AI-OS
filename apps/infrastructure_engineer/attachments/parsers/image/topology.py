from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import AttachmentMeta, InfrastructureAST
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class TopologyParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.attachment_type in {meta.attachment_type.diagram, meta.attachment_type.image} or meta.filename.lower().endswith((".svg", ".drawio", ".vsdx", ".png", ".jpg", ".jpeg", ".webp", ".bmp"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="topology")
        ast.system["diagram_format"] = meta.detected_format or meta.filename.lower()
        ast.system["ocr_or_structure_required"] = True
        return ast
