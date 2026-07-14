from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class DockerParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.docker or meta.filename.lower().endswith((".yml", ".yaml")) and "docker" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.docker, format="docker", device_role=meta.device_role)
        lowered = content.lower()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("FROM"):
                ast.system.setdefault("images", []).append(stripped[:200])
            if stripped.startswith("EXPOSE"):
                ast.services.append({"type": "port", "raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["privileged", "host network", "pid=host", "network_mode=host"]):
                ast.findings.append(InfrastructureFinding(Severity.high, "security", f"Container privilege escalation risk: {stripped}", "Review container isolation and security context", confidence=0.8))
        if "version:" in lowered and "services:" in lowered:
            ast.system["compose"] = True
        return ast
