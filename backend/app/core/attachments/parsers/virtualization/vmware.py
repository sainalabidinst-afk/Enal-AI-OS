from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class VmwareESXiParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.vmware or meta.filename.lower().endswith((".log", ".txt", ".json"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.vmware, format="esxi", device_role=meta.device_role)
        for line in content.splitlines()[:200]:
            if any(key in line.lower() for key in ["vm ", "virtual machine", "datastore", "snapshot", "ha ", "drs"]):
                ast.system.setdefault("vmware_signals", []).append(line.strip()[:200])
        return ast
