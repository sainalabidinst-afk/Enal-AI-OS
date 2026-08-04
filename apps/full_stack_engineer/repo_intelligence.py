"""
F0 — Repository Intelligence
=============================

Scans a repository and produces structured intelligence about:
- Languages, frameworks, architecture style
- Dependencies, entry points, build system, test system
- Containerization, CI/CD, documentation
- Project type classification

This is the foundational capability for all Full Stack Engineer modules.
Every other module (F1–F6) depends on F0's output for context-aware analysis.
"""

from apps.full_stack_engineer.repo_intelligence_models import (
    ARCHITECTURE_SIGNATURES,
    BUILD_SYSTEM_FILES,
    FRAMEWORK_SIGNATURES,
    IGNORE_DIRS,
    IGNORE_FILES,
    LanguageStat,
    RepositoryIntelligence,
    TEST_PATTERNS,
)
from apps.full_stack_engineer.repo_scanner import RepositoryScanner
from apps.full_stack_engineer.repo_engine import RepositoryIntelligenceEngine

repo_intelligence_engine = RepositoryIntelligenceEngine()
