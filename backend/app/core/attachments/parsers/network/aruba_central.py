from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class ArubaCentralParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.aruba and "central" in meta.text_preview.lower() or "aruba central" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.aruba, format="aruba_central", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "group" in stripped.lower() or "policy" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
        return ast
