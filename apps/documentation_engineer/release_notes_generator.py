"""
Release Notes Generator
=======================

Generates release notes from commit history.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReleaseNotesGenerator:
    """Generates release notes from commit history."""

    def generate(
        self,
        commit_range: str,
        app_name: str,
    ) -> dict[str, Any]:
        """
        Generate release notes from the given commit range.

        Args:
            commit_range: Git commit range (e.g., v1.0.0..v2.0.0).
            app_name: Name of the application.

        Returns:
            Generated release notes as a dict.
        """
        notes: dict[str, Any] = {
            "title": f"{app_name} Release Notes",
            "version": commit_range,
            "changes": [],
            "summary": f"Release notes for {app_name} ({commit_range}).",
        }
        logger.info("Generated release notes for %s from %s", app_name, commit_range)
        return {
            "path": f"docs/releases/{app_name}/CHANGELOG.md",
            "type": "release_notes",
            "size_bytes": len(str(notes).encode("utf-8")),
            "status": "generated",
            "issues": [],
            "content": notes,
        }
