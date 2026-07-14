from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class RuijieReyeeParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.ruijie and ("reyee" in meta.text_preview.lower() or "reyee" in meta.filename.lower())

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.ruijie, format="ruijie_reyee", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower() or "wlan" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "channel" in stripped.lower():
                ast.wireless.append({"type": "channel", "raw": stripped[:200]})
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
        return ast