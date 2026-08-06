from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import AttachmentMeta, InfrastructureAST
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class GrafanaParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.filename.lower().endswith((".json", ".txt")) and "grafana" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="grafana")
        for line in content.splitlines()[:200]:
            if any(key in line.lower() for key in ["dashboard", "alert", "panel", "query"]):
                ast.system.setdefault("monitoring", []).append(line.strip()[:200])
        return ast
