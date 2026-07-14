from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class CiscoASAParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.cisco and "asa" in meta.text_preview.lower() or meta.filename.lower().startswith("asa")

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.cisco, format="cisco_asa", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("hostname "):
                ast.system["hostname"] = stripped
            if stripped.startswith("interface "):
                ast.interfaces.append({"raw": stripped[:200]})
            if stripped.startswith("access-list ") or stripped.startswith("access-group "):
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("route "):
                ast.routing.append({"raw": stripped[:200]})
            if stripped.startswith("vpn "):
                ast.security.append({"raw": stripped[:200]})
        return ast
