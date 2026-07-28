from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class CambiumParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return "cambium" in meta.text_preview.lower() or "cambium" in meta.filename.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.ubiquiti, format="cambium", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower() or "wlan" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "channel" in stripped.lower():
                ast.wireless.append({"type": "channel", "raw": stripped[:200]})
        return ast
