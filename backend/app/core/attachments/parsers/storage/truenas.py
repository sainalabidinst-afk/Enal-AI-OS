from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class TrueNASParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.truenas or "truenas" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.truenas, format="truenas", device_role=meta.device_role)
        for line in content.splitlines()[:200]:
            if any(key in line.lower() for key in ["volume", "raid", "pool", "disk", "snapshot", "replication"]):
                ast.storage.append({"raw": line.strip()[:200]})
        return ast
