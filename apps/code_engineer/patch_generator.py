"""
Patch Generator
=================

Automated patch creation from refactoring suggestions and code changes.
Generates unified diffs, multi-file patch bundles, and validates patches.

Features:
- Unified diff generation (unified format)
- Multi-file patch bundling
- Rollback-ready patches
- Patch validation (syntax/compile check)
- Patch application preview
"""

import ast
import difflib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class PatchStatus:
    PENDING = "pending"
    VALIDATED = "validated"
    APPLIED = "applied"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class PatchHunk:
    """A single contiguous block of changes within a file."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    old_content: str
    new_content: str
    description: str = ""

    def to_unified_diff(self) -> str:
        """Generate unified diff format for this hunk."""
        header = f"@@ -{self.old_start},{self.old_count} +{self.new_start},{self.new_count} @@"
        if self.description:
            header += f" {self.description}"
        lines = [header]
        for line in self.old_content.splitlines(keepends=True):
            lines.append(f"-{line.rstrip()}")
        for line in self.new_content.splitlines(keepends=True):
            lines.append(f"+{line.rstrip()}")
        return "\n".join(lines)


@dataclass
class PatchFile:
    """Changes for a single file."""
    file_path: str
    hunks: list[PatchHunk] = field(default_factory=list)
    old_hash: str = ""
    new_hash: str = ""
    status: str = PatchStatus.PENDING
    validation_error: Optional[str] = None

    def to_unified_diff(self) -> str:
        """Generate full unified diff for this file."""
        if not self.hunks:
            return ""
        lines = [
            f"--- a/{self.file_path}",
            f"+++ b/{self.file_path}",
        ]
        for hunk in self.hunks:
            lines.append(hunk.to_unified_diff())
        return "\n".join(lines)

    def is_python_file(self) -> bool:
        return self.file_path.endswith(".py")


@dataclass
class PatchBundle:
    """A complete patch bundle with multiple file changes."""
    patch_id: str
    title: str
    description: str = ""
    files: list[PatchFile] = field(default_factory=list)
    author: str = "code-engineer"
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    status: str = PatchStatus.PENDING

    def to_unified_diff(self) -> str:
        """Generate complete unified diff for all files."""
        diff_parts = []
        for pf in self.files:
            fd = pf.to_unified_diff()
            if fd:
                diff_parts.append(fd)
        return "\n".join(diff_parts)

    def to_markdown(self) -> str:
        """Generate human-readable markdown summary."""
        lines = [
            f"# Patch Bundle: {self.title}",
            "",
            f"**ID**: {self.patch_id}",
            f"**Created**: {self.created_at}",
            f"**Status**: {self.status}",
            f"**Files**: {len(self.files)}",
            "",
        ]
        if self.description:
            lines.append(f"## Description\n\n{self.description}\n")

        for pf in self.files:
            added = sum(1 for h in pf.hunks for l in h.new_content.splitlines() if l.strip() and not l.strip().startswith('-'))
            removed = sum(1 for h in pf.hunks for l in h.old_content.splitlines() if l.strip() and not l.strip().startswith('+'))
            lines.append(f"## {pf.file_path}")
            lines.append(f"  - {len(pf.hunks)} hunks, +{added}/-{removed} lines")
            lines.append(f"  - Status: {pf.status}")
            for hunk in pf.hunks:
                if hunk.description:
                    lines.append(f"  - {hunk.description}")
            lines.append("")

        return "\n".join(lines)


class PatchGenerator:
    """Generates and manages code patches."""

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)
        self._patch_counter = 0

    async def generate_from_suggestion(
        self,
        file_path: str,
        suggestion: str,
        line_number: int,
        title: str = "",
        description: str = "",
    ) -> Optional[PatchBundle]:
        """Generate a patch from a text suggestion at a specific line."""
        full_path = self.repo_path / file_path
        if not full_path.exists():
            logger.error(f"File not found: {full_path}")
            return None

        try:
            content = full_path.read_text(encoding="utf-8")
            lines = content.splitlines(keepends=True)
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None

        # Create a hunk that replaces the target lines
        old_content = "".join(lines[line_number - 1:line_number]) if line_number <= len(lines) else ""

        bundle = self._create_bundle(title or f"Patch for {file_path}", description)
        patch_file = PatchFile(file_path=str(file_path))

        hunk = PatchHunk(
            old_start=line_number,
            old_count=1,
            new_start=line_number,
            new_count=1,
            old_content=old_content.rstrip(),
            new_content=suggestion,
            description=f"Apply suggestion at line {line_number}",
        )
        patch_file.hunks.append(hunk)
        bundle.files.append(patch_file)

        return bundle

    async def generate_from_changes(
        self,
        file_path: str,
        old_content: str,
        new_content: str,
        title: str = "",
        description: str = "",
    ) -> PatchBundle:
        """Generate a patch from old and new file content."""
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff = list(difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            n=3,
        ))

        bundle = self._create_bundle(title or f"Patch for {file_path}", description)
        patch_file = PatchFile(file_path=str(file_path))

        # Parse diff into hunks
        hunk_pattern = re.compile(r'^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@(.*)$')
        current_hunk: Optional[PatchHunk] = None
        old_lines_buffer: list[str] = []
        new_lines_buffer: list[str] = []

        for line in diff[2:]:  # Skip header lines
            match = hunk_pattern.match(line)
            if match:
                # Save previous hunk
                if current_hunk:
                    current_hunk.old_content = "".join(old_lines_buffer).rstrip()
                    current_hunk.new_content = "".join(new_lines_buffer).rstrip()
                    patch_file.hunks.append(current_hunk)

                old_start = int(match.group(1))
                old_count = int(match.group(2)) if match.group(2) else 1
                new_start = int(match.group(3))
                new_count = int(match.group(4)) if match.group(4) else 1
                desc = match.group(5).strip()

                current_hunk = PatchHunk(
                    old_start=old_start,
                    old_count=old_count,
                    new_start=new_start,
                    new_count=new_count,
                    old_content="",
                    new_content="",
                    description=desc,
                )
                old_lines_buffer = []
                new_lines_buffer = []
            elif current_hunk:
                if line.startswith('-') and not line.startswith('--'):
                    old_lines_buffer.append(line[1:])
                elif line.startswith('+') and not line.startswith('++'):
                    new_lines_buffer.append(line[1:])
                else:
                    old_lines_buffer.append(line)
                    new_lines_buffer.append(line)

        # Save last hunk
        if current_hunk:
            current_hunk.old_content = "".join(old_lines_buffer).rstrip()
            current_hunk.new_content = "".join(new_lines_buffer).rstrip()
            patch_file.hunks.append(current_hunk)

        bundle.files.append(patch_file)
        return bundle

    async def generate_refactoring_patch(
        self,
        file_path: str,
        line_number: int,
        old_code: str,
        new_code: str,
        description: str = "",
    ) -> PatchBundle:
        """Generate a patch for a refactoring change."""
        return await self.generate_from_changes(
            file_path=file_path,
            old_content=old_code,
            new_content=new_code,
            title=f"Refactoring: {description}",
            description=description,
        )

    async def validate_patch(self, bundle: PatchBundle) -> bool:
        """Validate a patch bundle (syntax check for Python files)."""
        all_valid = True

        for patch_file in bundle.files:
            if not patch_file.is_python_file():
                continue

            # Apply patch content to get new file content
            try:
                full_path = self.repo_path / patch_file.file_path
                if not full_path.exists():
                    patch_file.status = PatchStatus.FAILED
                    patch_file.validation_error = "File not found"
                    all_valid = False
                    continue

                original = full_path.read_text(encoding="utf-8")
                new_content = self._apply_patch_content(original, patch_file)

                if new_content is None:
                    patch_file.status = PatchStatus.FAILED
                    patch_file.validation_error = "Failed to apply patch"
                    all_valid = False
                    continue

                # Syntax check
                try:
                    ast.parse(new_content, filename=patch_file.file_path)
                    patch_file.status = PatchStatus.VALIDATED
                except SyntaxError as e:
                    patch_file.status = PatchStatus.FAILED
                    patch_file.validation_error = f"Syntax error: {e}"
                    all_valid = False

            except Exception as e:
                patch_file.status = PatchStatus.FAILED
                patch_file.validation_error = str(e)
                all_valid = False

        bundle.status = PatchStatus.VALIDATED if all_valid else PatchStatus.FAILED
        return all_valid

    def _create_bundle(self, title: str, description: str = "") -> PatchBundle:
        """Create a new patch bundle with unique ID."""
        self._patch_counter += 1
        return PatchBundle(
            patch_id=f"patch-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{self._patch_counter}",
            title=title,
            description=description,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def _apply_patch_content(self, original: str, patch_file: PatchFile) -> Optional[str]:
        """Apply patch hunks to original content and return new content."""
        lines = original.splitlines(keepends=True)
        # Apply hunks in reverse order to preserve line numbers
        for hunk in reversed(patch_file.hunks):
            old_start = hunk.old_start - 1  # Convert to 0-based
            old_count = hunk.old_count

            # Verify the old content matches
            old_lines = "".join(lines[old_start:old_start + old_count]).rstrip()
            if old_lines != hunk.old_content.rstrip():
                logger.warning(
                    f"Content mismatch at line {hunk.old_start}: "
                    f"expected {hunk.old_content!r}, got {old_lines!r}"
                )
                return None

            # Replace old lines with new lines
            new_lines_list = hunk.new_content.splitlines(keepends=True)
            lines[old_start:old_start + old_count] = new_lines_list

        return "".join(lines)

    async def apply_patch(self, bundle: PatchBundle) -> bool:
        """Apply a validated patch bundle to the repository."""
        if bundle.status != PatchStatus.VALIDATED:
            # Auto-validate first
            valid = await self.validate_patch(bundle)
            if not valid:
                return False

        all_applied = True
        for patch_file in bundle.files:
            if patch_file.status != PatchStatus.VALIDATED:
                continue

            try:
                full_path = self.repo_path / patch_file.file_path
                if not full_path.exists():
                    patch_file.status = PatchStatus.FAILED
                    patch_file.validation_error = "File not found"
                    all_applied = False
                    continue

                original = full_path.read_text(encoding="utf-8")
                new_content = self._apply_patch_content(original, patch_file)

                if new_content is None:
                    patch_file.status = PatchStatus.FAILED
                    patch_file.validation_error = "Failed to apply patch"
                    all_applied = False
                    continue

                # Write new content
                full_path.write_text(new_content, encoding="utf-8")
                patch_file.status = PatchStatus.APPLIED
                logger.info(f"Applied patch to {patch_file.file_path}")

            except Exception as e:
                patch_file.status = PatchStatus.FAILED
                patch_file.validation_error = str(e)
                all_applied = False

        bundle.status = PatchStatus.APPLIED if all_applied else PatchStatus.FAILED
        return all_applied

    async def rollback_patch(self, bundle: PatchBundle) -> bool:
        """Rollback an applied patch bundle."""
        all_rolled_back = True
        for patch_file in bundle.files:
            if patch_file.status != PatchStatus.APPLIED:
                continue

            try:
                full_path = self.repo_path / patch_file.file_path
                if not full_path.exists():
                    patch_file.status = PatchStatus.FAILED
                    all_rolled_back = False
                    continue

                original = full_path.read_text(encoding="utf-8")

                # Reverse the patch: swap old and new content
                reversed_file = PatchFile(file_path=patch_file.file_path)
                for hunk in patch_file.hunks:
                    reversed_hunk = PatchHunk(
                        old_start=hunk.new_start,
                        old_count=hunk.new_count,
                        new_start=hunk.old_start,
                        new_count=hunk.old_count,
                        old_content=hunk.new_content,
                        new_content=hunk.old_content,
                        description=f"Rollback: {hunk.description}",
                    )
                    reversed_file.hunks.append(reversed_hunk)

                restored = self._apply_patch_content(original, reversed_file)
                if restored is None:
                    patch_file.status = PatchStatus.FAILED
                    all_rolled_back = False
                    continue

                full_path.write_text(restored, encoding="utf-8")
                patch_file.status = PatchStatus.ROLLED_BACK
                logger.info(f"Rolled back patch on {patch_file.file_path}")

            except Exception:
                patch_file.status = PatchStatus.FAILED
                all_rolled_back = False

        bundle.status = PatchStatus.ROLLED_BACK if all_rolled_back else PatchStatus.FAILED
        return all_rolled_back

    async def preview_patch(self, bundle: PatchBundle) -> str:
        """Generate a preview of what the patch will do."""
        lines = [
            f"# Patch Preview: {bundle.title}",
            "",
            f"**Patch ID**: {bundle.patch_id}",
            f"**Files to modify**: {len(bundle.files)}",
            "",
        ]

        for patch_file in bundle.files:
            full_path = self.repo_path / patch_file.file_path
            exists = full_path.exists()
            lines.append(f"## {patch_file.file_path} {'(new file)' if not exists else ''}")
            lines.append(f"  - Hunks: {len(patch_file.hunks)}")

            total_added = 0
            total_removed = 0
            for hunk in patch_file.hunks:
                added = len([l for l in hunk.new_content.splitlines() if l.strip()])
                removed = len([l for l in hunk.old_content.splitlines() if l.strip()])
                total_added += added
                total_removed += removed
                if hunk.description:
                    lines.append(f"  - {hunk.description}")

            lines.append(f"  - +{total_added}/-{total_removed} lines")
            lines.append("")

        return "\n".join(lines)
