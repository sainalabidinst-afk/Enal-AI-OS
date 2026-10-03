"""
Cross-Pack Learner
==================

Learns reusable patterns across capability packs and generates
improvement proposals for Self Development.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

from apps.self_development.schemas import CrossPackPattern, ImprovementProposal, ProposalStatus

logger = logging.getLogger(__name__)


class CrossPackLearner:
    """Learns patterns across capability packs and proposes improvements."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(".").resolve()

    def learn(self) -> list[CrossPackPattern]:
        patterns: list[CrossPackPattern] = []

        pack_dirs = sorted([
            d for d in (self.root / "apps").iterdir()
            if d.is_dir() and not d.name.startswith("__pycache__") and d.name not in {"society", "organization", "integration"}
        ])

        common_modules = self._find_common_modules(pack_dirs)
        for module_name, packs in common_modules.items():
            if len(packs) >= 2:
                patterns.append(
                    CrossPackPattern(
                        id=f"pattern-{uuid.uuid4().hex[:8]}",
                        pattern_type=f"shared_{module_name}",
                        description=f"Shared {module_name} module across packs",
                        source_packs=[p.name for p in packs],
                        target_packs=[p.name for p in packs],
                        reusability_score=min(1.0, len(packs) / 5.0),
                        implementation_complexity="low" if len(packs) == 2 else "medium",
                    )
                )

        common_tools = self._find_common_tools(pack_dirs)
        for tool_name, packs in common_tools.items():
            if len(packs) >= 2:
                patterns.append(
                    CrossPackPattern(
                        id=f"pattern-{uuid.uuid4().hex[:8]}",
                        pattern_type=f"shared_tool_{tool_name}",
                        description=f"Shared tool {tool_name} across packs",
                        source_packs=[p.name for p in packs],
                        target_packs=[p.name for p in packs],
                        reusability_score=min(1.0, len(packs) / 5.0),
                        implementation_complexity="low",
                    )
                )

        return patterns

    def propose_extractions(self, patterns: list[CrossPackPattern]) -> list[ImprovementProposal]:
        proposals: list[ImprovementProposal] = []
        for pattern in patterns:
            if pattern.reusability_score >= 0.6:
                proposals.append(
                    ImprovementProposal(
                        id=f"imp-{uuid.uuid4().hex[:8]}",
                        target_type="cross_pack",
                        target_id=pattern.id,
                        improvement_type="refactor",
                        description=f"Extract shared {pattern.pattern_type} into core module",
                        estimated_effort="medium",
                        risk="low",
                        confidence=0.8,
                        expected_impact=f"Reduce duplication across {len(pattern.source_packs)} packs",
                    )
                )
        return proposals

    def _find_common_modules(self, pack_dirs: list[Path]) -> dict[str, list[Path]]:
        common: dict[str, list[Path]] = {}
        module_names = ["engine.py", "worker.py", "schemas.py", "attachments", "knowledge"]

        for module_name in module_names:
            matching_packs: list[Path] = []
            for pack_dir in pack_dirs:
                if (pack_dir / module_name).exists():
                    matching_packs.append(pack_dir)
            if matching_packs:
                common[module_name] = matching_packs

        return common

    def _find_common_tools(self, pack_dirs: list[Path]) -> dict[str, list[Path]]:
        common: dict[str, list[Path]] = {}
        tool_names = ["analyzer", "scanner", "validator", "parser"]

        for tool_name in tool_names:
            matching_packs: list[Path] = []
            for pack_dir in pack_dirs:
                for f in pack_dir.rglob(f"*{tool_name}*.py"):
                    if f.is_file():
                        matching_packs.append(pack_dir)
                        break
            if matching_packs:
                common[tool_name] = matching_packs

        return common
