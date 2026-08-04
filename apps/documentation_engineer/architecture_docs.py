"""
Architecture Documentation Generator
=====================================

Generates architecture documentation from ADRs, RFCs, and source code.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ArchitectureDocsGenerator:
    """Generates architecture documentation from ADRs, RFCs, and code."""

    def generate(
        self,
        source_code_path: str,
        architecture_artifacts: list[str],
    ) -> dict[str, Any]:
        """
        Generate architecture documentation.

        Args:
            source_code_path: Path to the source code directory.
            architecture_artifacts: List of ADR/RFC file paths.

        Returns:
            Generated architecture documentation as a dict.
        """
        docs: dict[str, Any] = {
            "title": "Architecture Documentation",
            "overview": "Auto-generated architecture documentation from ADRs and RFCs.",
            "decisions": [],
            "components": [],
            "diagrams": [],
        }
        for artifact in architecture_artifacts:
            docs["decisions"].append(
                {"source": artifact, "summary": "Architecture decision record."}
            )
        logger.info("Generated architecture docs from %d artifacts", len(architecture_artifacts))
        return {
            "path": "docs/architecture/overview.md",
            "type": "architecture",
            "size_bytes": len(str(docs).encode("utf-8")),
            "status": "generated",
            "issues": [],
            "content": docs,
        }
