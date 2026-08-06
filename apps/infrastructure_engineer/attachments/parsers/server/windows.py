from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class WindowsParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.windows or meta.filename.lower().endswith((".ps1", ".txt", ".log", ".xml"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.windows, format="windows", device_role=meta.device_role)
        lowered = content.lower()
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if any(key in lowered for key in ["ipconfig", "get-netadapter", "netstat"]):
                ast.interfaces.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["get-service", "iis", "microsoft-aspnetcore"]):
                ast.services.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["user ", "group ", "gpo", "active directory"]):
                ast.security.append({"raw": stripped[:200]})
            if "firewall" in stripped.lower():
                ast.firewall.append({"raw": stripped[:200]})
        return ast
