"""
Repository Intelligence Engine
================================

Engine that orchestrates repository intelligence gathering.
"""

from typing import Any

from apps.full_stack_engineer.repo_intelligence_models import RepositoryIntelligence
from apps.full_stack_engineer.repo_scanner import RepositoryScanner


class RepositoryIntelligenceEngine:
    """Engine that orchestrates repository intelligence gathering."""

    async def analyze(self, repo_path: str) -> dict[str, Any]:
        """Analyze a repository and return structured intelligence."""
        scanner = RepositoryScanner(repo_path)
        info = scanner.scan()
        return info.to_dict()

    async def analyze_markdown(self, repo_path: str) -> str:
        """Analyze a repository and return a Markdown report."""
        scanner = RepositoryScanner(repo_path)
        info = scanner.scan()
        return info.to_markdown()


repo_intelligence_engine = RepositoryIntelligenceEngine()
