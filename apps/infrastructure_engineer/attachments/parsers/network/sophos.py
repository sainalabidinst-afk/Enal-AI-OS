from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class SophosParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.sophos or "sophos" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.sophos, format="sophos", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "hostname" in stripped.lower():
                ast.system["hostname"] = stripped
            if "interface" in stripped.lower():
                ast.interfaces.append({"raw": stripped[:200]})
            if "firewall" in stripped.lower() or "rule" in stripped.lower():
                ast.firewall.append({"raw": stripped[:200]})
            if "vpn" in stripped.lower() or "ipsec" in stripped.lower():
                ast.security.append({"raw": stripped[:200]})
            if "wlan" in stripped.lower() or "ssid" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
        return ast
