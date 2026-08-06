from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class UniFiParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.ubiquiti and "unifi" in meta.text_preview.lower() or "unifi" in meta.filename.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.ubiquiti, format="unifi", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower() or "wlan" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
            if "firewall" in stripped.lower() or "policy" in stripped.lower():
                ast.firewall.append({"raw": stripped[:200]})
        return ast
