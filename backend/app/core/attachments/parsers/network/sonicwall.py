from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class SonicWallParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.sonicwall or "sonicwall" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.sonicwall, format="sonicos", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("set hosts name"):
                ast.system["hostname"] = stripped
            if stripped.startswith("add interface "):
                ast.interfaces.append({"raw": stripped[:200]})
            if stripped.startswith("add firewall "):
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("add vpn "):
                ast.security.append({"raw": stripped[:200]})
            if stripped.startswith("add zone "):
                ast.security.append({"raw": stripped[:200]})
        return ast
