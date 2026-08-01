"""
System Architect — ADR Generator.

Generates Architecture Decision Records (ADR) from architectural analysis:
- Standard ADR template (context, decision, consequences)
- Context-aware content synthesis from findings
- Status tracking (proposed → accepted/rejected)
- Consistency with existing ADR numbering
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apps.system_architect.schemas import (
    ADRDraft,
    ADRStatus,
    Finding,
)

logger = logging.getLogger(__name__)


class ADRGenerator:
    """
    Generates structured ADR drafts from architectural findings.

    Usage::
        generator = ADRGenerator(existing_adrs)
        adr = generator.generate(title, context, findings)
    """

    ADR_TEMPLATE_HEADER = """# ADR-{number}: {title}

| Field | Value |
|-------|-------|
| **Status** | {status} |
| **Date** | {date} |
| **Author** | Enal AI OS System Architect |

---

## Context

{context}

## Decision

{decision}

## Consequences

{consequences}
"""

    def __init__(self, existing_adrs: list[str] | None = None, adr_dir: str | Path | None = None):
        self.existing_adrs = existing_adrs or []
        self.adr_dir = Path(adr_dir) if adr_dir else None
        self._next_number = self._determine_next_number()

    def _determine_next_number(self) -> int:
        """Determine next ADR number based on existing ADRs."""
        max_num = 0
        pattern = re.compile(r"ADR[-_]?(\d+)", re.IGNORECASE | re.UNICODE)
        for ref in self.existing_adrs:
            match = pattern.search(ref)
            if match:
                max_num = max(max_num, int(match.group(1)))
        # Also scan the ADR directory if available
        if self.adr_dir and self.adr_dir.exists():
            for f in self.adr_dir.iterdir():
                match = pattern.search(f.name)
                if match:
                    max_num = max(max_num, int(match.group(1)))
        return max_num + 1

    def generate(
        self,
        title: str,
        context: str,
        findings: list[Finding] | None = None,
        decision: str | None = None,
        consequences: list[str] | None = None,
    ) -> ADRDraft:
        """Generate an ADR draft from context and findings."""
        findings = findings or []
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Synthesize decision and consequences from findings
        if decision is None:
            decision = self._synthesize_decision(title, findings)
        if consequences is None:
            consequences = self._synthesize_consequences(findings)

        adr = ADRDraft(
            title=f"ADR-{self._next_number}: {title}",
            status=ADRStatus.proposed,
            context=context,
            decision=decision,
            consequences=consequences,
        )
        self._next_number += 1
        return adr

    def to_markdown(self, adr: ADRDraft) -> str:
        """Render an ADRDraft as markdown text."""
        # Extract number from title if present
        match = re.search(r"ADR[-_]?(\d+)", adr.title)
        number = match.group(1) if match else str(self._next_number - 1)
        title_clean = re.sub(r"^ADR[-_]?\d+[: ]*", "", adr.title)

        consequences = "\n".join(f"- {c}" for c in adr.consequences) or "- (none)"

        return self.ADR_TEMPLATE_HEADER.format(
            number=number,
            title=title_clean,
            status=adr.status.value,
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            context=adr.context,
            decision=adr.decision,
            consequences=consequences,
        )

    def generate_from_report(
        self,
        title: str,
        context: str,
        findings: list[Finding],
        focus_categories: list[Any] | None = None,
    ) -> ADRDraft:
        """Generate an ADR from review findings, optionally filtered by category."""
        if focus_categories:
            findings = [f for f in findings if f.category in focus_categories]
        return self.generate(title=title, context=context, findings=findings)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _synthesize_decision(self, title: str, findings: list[Finding]) -> str:
        """Synthesize a decision statement from findings."""
        if findings:
            criticals = [f for f in findings if f.severity.value == "critical"]
            highs = [f for f in findings if f.severity.value == "high"]
            if criticals:
                top = criticals[0]
            elif highs:
                top = highs[0]
            else:
                top = findings[0]
            severity = top.severity.value.upper()
            return (
                f"We will address the {severity} issue(s) identified in the "
                f"architecture review — particularly {top.title.lower()}. "
                "The resolution approach will be implemented within the affected "
                "Capability Pack and validated by benchmark regression."
            )
        return (
            f"No critical architectural findings; we will maintain the current "
            f"architecture for {title} while monitoring benchmarks."
        )

    def _synthesize_consequences(self, findings: list[Finding]) -> list[str]:
        """Synthesize positive and negative consequences."""
        consequences: list[str] = []
        if findings:
            severity_map: dict[str, int] = {}
            for f in findings:
                severity_map[f.severity.value] = severity_map.get(f.severity.value, 0) + 1
            summary = ", ".join(f"{v} {k}" for k, v in sorted(severity_map.items()))
            consequences.append(
                f"Addressing {len(findings)} architectural finding(s) ({summary}) "
                "improves maintainability and reduces technical debt."
            )
            consequences.append(
                "Changes will be contained within Capability Packs; Core remains frozen."
            )
        else:
            consequences.append("No immediate architectural change required.")
            consequences.append("Architecture quality is maintained via periodic reviews.")
        return consequences

    def save(self, adr: ADRDraft, directory: str | Path | None = None) -> Path:
        """Persist an ADR draft to disk as markdown."""
        target = Path(directory) if directory else self.adr_dir
        if target is None:
            raise ValueError("No ADR directory specified; pass `directory` or set adr_dir.")
        target.mkdir(parents=True, exist_ok=True)

        match = re.search(r"ADR[-_]?(\d+)", adr.title)
        number = match.group(1) if match else str(self._next_number - 1)
        short_title = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^ADR[-_]?\d+[: ]*", "", adr.title).lower()).strip("-")
        filename = f"ADR-{number}-{short_title}.md"
        path = target / filename
        path.write_text(self.to_markdown(adr), encoding="utf-8")
        return path

