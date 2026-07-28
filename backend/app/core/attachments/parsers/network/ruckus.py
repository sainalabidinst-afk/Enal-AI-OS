from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class RuckusParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return "ruckus" in meta.text_preview.lower() or meta.vendor == VendorFamily.extreme and "ruckus" in meta.filename.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.extreme, format="ruckus", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower() or "wlan" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "channel" in stripped.lower():
                ast.wireless.append({"type": "channel", "raw": stripped[:200]})
            if "mesh" in stripped.lower():
                ast.wireless.append({"type": "mesh", "raw": stripped[:200]})
        return ast
