from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class OmadaParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return "omada" in meta.text_preview.lower() or "tp-link" in meta.text_preview.lower() and "omada" in meta.filename.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.ubiquiti, format="omada", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
        return ast