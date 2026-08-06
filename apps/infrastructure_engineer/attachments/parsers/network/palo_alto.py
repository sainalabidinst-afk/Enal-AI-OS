from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class PaloAltoParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.palo_alto or meta.filename.lower().endswith((".conf", ".txt", ".xml"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.palo_alto, format="pan_os", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("set deviceconfig system hostname"):
                ast.system["hostname"] = stripped
            if stripped.startswith("set interface "):
                ast.interfaces.append({"raw": stripped[:200]})
            if stripped.startswith("set virtual-router "):
                ast.routing.append({"raw": stripped[:200]})
            if stripped.startswith("set security "):
                if "policy" in stripped.lower():
                    ast.firewall.append({"raw": stripped[:200]})
                if "nat" in stripped.lower():
                    ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("set zone "):
                ast.security.append({"raw": stripped[:200]})
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
        return ast
