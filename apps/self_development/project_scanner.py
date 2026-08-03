"""
Project Scanner
===============

AST-based project structure analysis for Self Development.

Collects module/file counts, hotspot candidates, and basic
complexity signals without mutating the source tree.
"""

from __future__ import annotations

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from apps.self_development.schemas import ProjectAnalysis

logger = logging.getLogger(__name__)

HOTSPOT_CANDIDATES: list[str] = [
    "communication.py",
    "team_builder.py",
    "agent_registry.py",
    "orchestrator_v2.py",
    "cognitive_kernel.py",
    "model_router.py",
    "memory_layer.py",
    "artifact_service.py",
    "workspace_service.py",
    "stream_handler.py",
    "execution_integration.py",
]


@dataclass
class ProjectScanResult:
    project: str
    modules_count: int
    files_count: int
    complexity: str
    language: str = "python"
    framework: str = ""
    hotspots: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ProjectScanner:
    """Scans a project directory for structure and hotspot candidates."""

    def scan(self, project_path: str) -> ProjectScanResult:
        base = Path(project_path)
        hotspots: list[str] = []
        files_count = 0
        modules_count = 0
        complexity = "medium"

        try:
            py_files = list(base.rglob("*.py"))
            files_count = len(py_files)
            modules_count = len({f.parent.name for f in py_files if f.parent != base})
            hotspots = [name for name in HOTSPOT_CANDIDATES if any(f.name == name for f in py_files)]
            if any(f.name == "orchestrator_v2.py" for f in py_files):
                complexity = "high"
            if modules_count > 20:
                complexity = "high"
        except Exception:
            logger.debug("Project scan failed; using defaults", exc_info=True)

        return ProjectScanResult(
            project=base.name or "Enal AI OS",
            modules_count=modules_count,
            files_count=files_count,
            complexity=complexity,
            language="python",
            framework="ECP",
            hotspots=hotspots,
        )

    def to_analysis(self, result: ProjectScanResult) -> ProjectAnalysis:
        return ProjectAnalysis(
            project=result.project,
            modules_count=result.modules_count,
            files_count=result.files_count,
            complexity=result.complexity,
            language=result.language,
            framework=result.framework,
            metadata={"hotspots": result.hotspots},
        )


def analyze_project(project_path: str | None = None) -> dict[str, Any]:
    project_path = project_path or str(Path(__file__).resolve().parent.parent.parent)
    scanner = ProjectScanner()
    result = scanner.scan(project_path)
    return {
        "project": result.project,
        "modules_count": result.modules_count,
        "files_count": result.files_count,
        "complexity": result.complexity,
        "language": result.language,
        "framework": result.framework,
        "hotspots": result.hotspots,
    }
