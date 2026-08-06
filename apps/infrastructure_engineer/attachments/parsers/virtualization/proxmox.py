from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class ProxmoxParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.proxmox or "proxmox" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.proxmox, format="proxmox", device_role=meta.device_role)
        for line in content.splitlines()[:200]:
            if any(key in line.lower() for key in ["vm ", "lxc", "storage", "network", "snapshot"]):
                ast.system.setdefault("proxmox_signals", []).append(line.strip()[:200])
        return ast
