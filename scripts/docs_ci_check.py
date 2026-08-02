"""
Documentation CI — Automated documentation consistency checks.

Run this script in CI to verify:
- No broken markdown links
- Consistent Capability Pack count (current state = 13)
- No nested translation layers
- All docs have metadata blocks
- No stale dates

Usage:
    python scripts/docs_ci_check.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_FILES = list(REPO_ROOT.rglob("*.md"))

CURRENT_PACK_COUNT = 13
EXPECTED_DATE = "2026-08-02"
TECHNICAL_TERMS = {
    "Capability Pack", "Golden Test", "Benchmark", "Plugin", "Runtime", "Worker",
    "Core", "Architecture", "API", "SDK", "Docker", "FastAPI", "Redis",
    "PostgreSQL", "Qdrant", "MinIO", "Ollama", "Claude", "Gemini", "OpenAI",
    "RFC", "ADR", "Prompt", "Context", "Memory", "Reasoning", "Decision",
    "Planning", "Knowledge Graph", "Capability Graph", "Execution Runtime",
    "ECP", "Enal AI OS", "Enal Cognitive Platform",
}


def check_pack_count(file_path: Path) -> list[str]:
    """Check for inconsistent Capability Pack counts."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    # Look for pack count mentions
    patterns = [
        (r"\b(\d+)\s+Capability Pack[s]?\b", "Capability Pack count"),
        (r"\b(\d+)\s+pack[s]?\s+certified\b", "packs certified"),
        (r"\b(\d+)\s+pack[s]?\s+existing\b", "packs existing"),
        (r"\b(\d+)\s+Paket\s+Kemampuan\b", "Paket Kemampuan count"),
    ]

    # Skip roadmap files for pack count checks (they contain future targets)
    roadmap_indicators = ["roadmap", "v1_roadmap", "ROADMAP", "TODO_CAPABILITY"]
    is_roadmap = any(indicator in file_path.name for indicator in roadmap_indicators)

    if not is_roadmap:
        for pattern, desc in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                # Verify match is on a single line (no newlines in match)
                matched_text = match.group(0)
                if '\n' in matched_text:
                    continue
                # Skip ADR-XXX references (e.g., "ADR-002 Capability Pack Independence")
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_text = content[line_start:content.find('\n', match.start())]
                if re.search(r'ADR[\s-]?\d+\s+Capability Pack', line_text, re.IGNORECASE):
                    continue
                count = int(match.group(1))
                if count != CURRENT_PACK_COUNT:
                    line_num = content[:match.start()].count("\n") + 1
                    issues.append(
                        f"Line {line_num}: {desc} = {count} (expected {CURRENT_PACK_COUNT})"
                    )

    return issues


def check_nested_translations(file_path: Path) -> list[str]:
    """Check for nested translation layers."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        if "> > Bahasa Indonesia:" in line:
            issues.append(f"Line {i}: Triple-nested translation found")

    return issues


CANONICAL_DOCS = {
    "README.md",
    "docs/CAPABILITY_GUIDE.md",
    "docs/RELEASE_CRITERIA.md",
    "docs/v1_roadmap.md",
    "docs/CAPABILITY_STRATEGY.md",
    "docs/ROADMAP.md",
    "docs/ARCHITECTURE_DECISIONS.md",
    "docs/rfcs/README.md",
    "docs/architecture.md",
    "docs/GOVERNANCE_CHARTER.md",
    "docs/GOVERNANCE.md",
    "docs/BILINGUAL_DOCUMENTATION.md",
    "VERSION_MATRIX.md",
    "TODO_CAPABILITY_EXECUTION.md",
    "docs/ENGINEERING_BASELINE.md",
    "docs/QUALITY_GATE.md",
    "docs/PRODUCT_CONTRACT.md",
}


def check_metadata(file_path: Path) -> list[str]:
    """Check for Document Owner metadata on canonical docs only."""
    issues = []
    rel_path = str(file_path.relative_to(REPO_ROOT)).replace("\\", "/")
    
    # Only check metadata for canonical docs
    if rel_path not in CANONICAL_DOCS:
        return issues
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    if "<!-- DOCUMENT_METADATA_START -->" not in content:
        issues.append("Missing DOCUMENT_METADATA block")

    return issues


def check_broken_links(file_path: Path) -> list[str]:
    """Check for broken relative markdown links."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    # Find all markdown links
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for match in link_pattern.finditer(content):
        link_path = match.group(2)
        if link_path.startswith(("http://", "https://", "#", "mailto:")):
            continue

        # Resolve relative path
        if link_path.startswith("/"):
            resolved = REPO_ROOT / link_path[1:]
        else:
            resolved = file_path.parent / link_path

        if not resolved.exists():
            line_num = content[:match.start()].count("\n") + 1
            issues.append(f"Line {line_num}: Broken link [{match.group(1)}]({link_path})")

    return issues


def check_stale_dates(file_path: Path) -> list[str]:
    """Check for stale dates in metadata."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    # Look for date patterns in metadata
    date_pattern = re.compile(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})")
    for match in date_pattern.finditer(content):
        date = match.group(1)
        if date < EXPECTED_DATE:
            line_num = content[:match.start()].count("\n") + 1
            issues.append(f"Line {line_num}: Stale date {date} (expected >= {EXPECTED_DATE})")

    return issues


def main() -> int:
    all_issues: dict[str, list[str]] = {}
    total_issues = 0

    print("=" * 70)
    print("Documentation CI Check")
    print("=" * 70)
    print(f"Checking {len(MD_FILES)} markdown files...\n")

    for md_file in MD_FILES:
        # Skip hidden directories and external dependencies
        skip_dirs = {".venv", "node_modules", "__pycache__", ".git", "dist", "build", ".next"}
        if any(part in skip_dirs for part in md_file.parts):
            continue

        # Skip audit/report files (they document historical state)
        skip_files = {
            "DOCUMENTATION_CONSISTENCY_AUDIT_REPORT.md",
            "ARCHITECTURE_CONSISTENCY_REPORT.md",
            "FINAL_REPOSITORY_AUDIT.md",
            "QUALITY_REMEDIATION_REPORT.md",
            "TYPE_FIX_REPORT.md",
            "WORKFLOW_CATALOG_REPORT.md",
            "PLAN_DOKUMENTASI_CONSISTENCY.md",
            "PLAN_RFC-0007.md",
            "PLAN_RFC-0011.md",
        }
        if md_file.name in skip_files:
            continue

        rel_path = md_file.relative_to(REPO_ROOT)
        file_issues: list[str] = []

        file_issues.extend(check_pack_count(md_file))
        file_issues.extend(check_nested_translations(md_file))
        file_issues.extend(check_metadata(md_file))
        file_issues.extend(check_broken_links(md_file))
        file_issues.extend(check_stale_dates(md_file))

        if file_issues:
            all_issues[str(rel_path)] = file_issues
            total_issues += len(file_issues)

    if all_issues:
        print(f"FAIL: Found {total_issues} issues in {len(all_issues)} files:\n")
        for file_path, issues in all_issues.items():
            print(f"\n{file_path}:")
            for issue in issues:
                print(f"  - {issue}")
        sys.stdout.flush()
        return 1

    print("PASS: All documentation checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
