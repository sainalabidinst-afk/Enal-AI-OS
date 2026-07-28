from __future__ import annotations

from backend.app.core.attachments.models import AttachmentMeta, InfrastructureAST
from backend.app.core.attachments.parsers.base import BaseParser


class ScreenshotParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.attachment_type in {meta.attachment_type.image, meta.attachment_type.screenshot}

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="screenshot", device_role=meta.device_role)
        ast.system["image_kind"] = "screenshot"
        ast.system["ocr_required"] = True
        ast.system["likely_vendors"] = ["winbox", "fortigate", "unifi", "aruba", "esxi", "proxmox", "idrac"]
        return ast
