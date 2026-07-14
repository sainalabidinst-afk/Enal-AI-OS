from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class KubernetesParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.kubernetes or "apiVersion" in meta.text_preview or "kind:" in meta.text_preview

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.kubernetes, format="kubernetes", device_role=meta.device_role)
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("apiVersion:"):
                ast.system.setdefault("api_versions", []).append(stripped[:200])
            if stripped.startswith("kind:"):
                ast.system.setdefault("kinds", []).append(stripped[:200])
            if any(key in stripped.lower() for key in ["hostpath", "privileged", "runasuser=0", "cap_add", "privileged"]):
                ast.findings.append(InfrastructureFinding(Severity.high, "security", f"Kubernetes security risk: {stripped}", "Review pod security context and RBAC", confidence=0.8))
        return ast
