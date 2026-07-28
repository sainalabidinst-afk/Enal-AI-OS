from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class CheckPointParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.checkpoint or "check point" in meta.text_preview.lower() or "cp-".lower() in meta.filename.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.checkpoint, format="checkpoint", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("set hostname"):
                ast.system["hostname"] = stripped
            if "interface" in stripped.lower() or "ip addr" in stripped.lower():
                ast.interfaces.append({"raw": stripped[:200]})
            if "rule" in stripped.lower() or "policy" in stripped.lower():
                ast.firewall.append({"raw": stripped[:200]})
            if "vpn" in stripped.lower() or "tunnel" in stripped.lower():
                ast.security.append({"raw": stripped[:200]})
        return ast
