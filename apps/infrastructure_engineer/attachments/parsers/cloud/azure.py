from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class AzureParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.azure or "azurerm" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.azure, format="cloud", device_role=meta.device_role)
        for line in content.splitlines()[:200]:
            if any(key in line.lower() for key in ["azurerm_", "resource ", "data "]):
                ast.system.setdefault("cloud_resources", []).append(line.strip()[:200])
        return ast
