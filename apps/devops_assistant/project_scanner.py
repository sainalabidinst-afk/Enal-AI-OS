"""
DevOps Project Scanner
======================

Scans project files for DevOps-relevant configurations and artifacts.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from apps.devops_assistant.schemas import ProjectAnalysis

logger = logging.getLogger(__name__)

DEVOPS_EXTENSIONS: set[str] = {
    ".yml",
    ".yaml",
    ".json",
    ".tf",
    ".hcl",
    ".dockerfile",
    "Dockerfile",
    "Jenkinsfile",
}
DEVOPS_DIRECTORIES: set[str] = {
    ".github",
    ".gitlab",
    "k8s",
    "kubernetes",
    "terraform",
    "helm",
    "monitoring",
}


class DevOpsProjectScanner:
    """Scans project for DevOps configurations."""

    def scan(self, project_path: str) -> ProjectAnalysis:
        if not os.path.isdir(project_path):
            raise FileNotFoundError(f"Project path not found: {project_path}")

        files_count = 0
        modules_count = 0
        devops_files: list[str] = []
        languages: set[str] = set()
        frameworks: set[str] = set()

        for root, dirs, files in os.walk(project_path):
            for file in files:
                files_count += 1
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                ext = ext.lower()

                if ext in DEVOPS_EXTENSIONS or file in ("Jenkinsfile", "Dockerfile"):
                    devops_files.append(file_path)

                if file == "package.json":
                    languages.add("javascript")
                elif file == "requirements.txt" or file == "pyproject.toml":
                    languages.add("python")
                elif file == "go.mod":
                    languages.add("go")
                elif file == "pom.xml":
                    languages.add("java")

        for directory in DEVOPS_DIRECTORIES:
            if os.path.isdir(os.path.join(project_path, directory)):
                modules_count += 1

        if os.path.exists(os.path.join(project_path, "terraform")) or any(
            f.endswith(".tf") for f in devops_files
        ):
            frameworks.add("terraform")
        if os.path.exists(os.path.join(project_path, "k8s")) or os.path.exists(
            os.path.join(project_path, "kubernetes")
        ):
            frameworks.add("kubernetes")
        if os.path.exists(os.path.join(project_path, ".github")):
            frameworks.add("github_actions")
        if os.path.exists(os.path.join(project_path, ".gitlab")):
            frameworks.add("gitlab_ci")

        complexity = self._assess_complexity(files_count, modules_count, len(devops_files))
        return ProjectAnalysis(
            project=os.path.basename(project_path),
            modules_count=modules_count,
            files_count=files_count,
            complexity=complexity,
            language=", ".join(sorted(languages)) if languages else "unknown",
            framework=", ".join(sorted(frameworks)) if frameworks else "",
            metadata={"devops_files_count": len(devops_files), "devops_files": devops_files[:10]},
        )

    def _assess_complexity(self, files_count: int, modules_count: int, devops_files_count: int) -> str:
        score = files_count * 0.1 + modules_count * 2 + devops_files_count * 0.5
        if score > 50:
            return "high"
        if score > 20:
            return "medium"
        return "low"
