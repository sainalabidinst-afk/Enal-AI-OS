"""
Governance Enforcement Checks
==============================

Implements CI/CD checks for ECP governance rules per docs/GOVERNANCE.md:

1. Core Change Protection (Section 4, 6)
   - Detects modifications to core directories without ADR reference
   
2. Capability First Rule (Section 1)
   - Detects capability packs importing from other capability packs
   
3. ADR Reference Check (Section 6)
   - Ensures core changes reference an approved ADR

Usage:
    python benchmarks/governance_checks.py [--check-core] [--check-imports]
"""

from __future__ import annotations

import argparse
import ast
import logging
import re
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Core directories that require ADR approval for modifications
CORE_PATHS = [
    "backend/app/core",
    "backend/app/kernel",
    "backend/app/runtime",
    "backend/app/sdk",
    "sdk/",
    "backend/app/contracts",
]

# Capability packs - importing between these is forbidden
CAPABILITY_PACKS = [
    "trading_analyst",
    "network_engineer",
    "devops_assistant",
    "code_engineer",
    "research_assistant",
    "full_stack_engineer",
    "self_development",
    "decision_intelligence",
    "system_architect",
    "security_engineer",
    "data_engineer",
    "database_engineer",
    "qa_engineer",
    "business_analyst",
    "documentation_engineer",
    "product_manager",
    "infrastructure_engineer",
    "ai_engineer",
    "ui_ux_designer",
    "cloud_architect",
    "sre_engineer",
    "compliance_officer",
    "knowledge_engineer",
    "finance_analyst",
    "legal_advisor",
    "hse_specialist",
    "observability",
    "cybersecurity_analyst",
    "ai_ethics_pack",
    "supply_chain_analyst",
    "data_scientist",
    "business_intelligence",
    "innovation_strategist",
    "devsecops",
    "translator_expert",
    "document_processing",
    "voice_interaction",
]

# ADR file pattern
ADR_PATTERN = re.compile(r"docs/adr/ADR-\d+.*\.md")

# Core file pattern to detect git changes
CORE_FILE_PATTERN = re.compile(
    r"^backend/app/(core|kernel|runtime|sdk|contracts)/|sdk/",
)


def get_changed_files() -> list[str]:
    """Get list of files changed in the current git diff (staged + unstaged)."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        return files
    except Exception as e:
        logger.debug(f"Could not get git diff: {e}")
        return []


def check_core_changes(files: list[str]) -> list[dict[str, str]]:
    """Check if core directories are modified without ADR reference."""
    violations = []
    core_files_changed = [
        f for f in files if CORE_FILE_PATTERN.match(f) or f.startswith("sdk/")
    ]

    if not core_files_changed:
        return violations

    # Check if any changed file path contains ADR reference
    has_adr_reference = any(ADR_PATTERN.search(f) for f in files)

    if not has_adr_reference:
        for f in core_files_changed:
            violations.append({
                "rule": "core_change_protection",
                "file": f,
                "message": f"Core file '{f}' modified without ADR reference. "
                f"Add an ADR in docs/adr/ and reference it in your commit message.",
            })

    return violations


def check_cross_capability_imports(root_path: str = ".") -> list[dict[str, str]]:
    """Check for direct imports between capability packs using AST analysis."""
    violations = []
    root = Path(root_path)

    apps_dir = root / "apps"
    if not apps_dir.exists():
        return violations

    for pack_dir in apps_dir.iterdir():
        if not pack_dir.is_dir() or pack_dir.name.startswith("_"):
            continue

        source_pack = pack_dir.name
        if source_pack not in CAPABILITY_PACKS:
            continue

        for py_file in pack_dir.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue

            # Skip the apps/__init__.py which legitimately loads all packs
            if py_file.name == "__init__.py" and py_file.parent == apps_dir:
                continue

            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(content)
            except Exception:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name
                        if module.startswith("apps."):
                            for pack in CAPABILITY_PACKS:
                                if module == f"apps.{pack}" or module.startswith(f"apps.{pack}."):
                                    if pack != source_pack:
                                        violations.append({
                                            "rule": "capability_first_rule",
                                            "source_pack": source_pack,
                                            "target_pack": pack,
                                            "file": str(py_file.relative_to(root)),
                                            "line": node.lineno,
                                            "message": f"Capability '{source_pack}' imports from capability '{pack}'. "
                                            f"Use Execution Runtime and shared contracts instead.",
                                        })

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    if module.startswith("apps."):
                        for pack in CAPABILITY_PACKS:
                            if module == f"apps.{pack}" or module.startswith(f"apps.{pack}."):
                                if pack != source_pack:
                                    violations.append({
                                        "rule": "capability_first_rule",
                                        "source_pack": source_pack,
                                        "target_pack": pack,
                                        "file": str(py_file.relative_to(root)),
                                        "line": node.lineno,
                                        "message": f"Capability '{source_pack}' imports from capability '{pack}'. "
                                        f"Use Execution Runtime and shared contracts instead.",
                                    })

    return violations


def check_package_boundaries() -> list[dict[str, str]]:
    """Run the existing package boundary check."""
    try:
        result = subprocess.run(
            [sys.executable, str(Path("benchmarks/package_boundaries.py"))],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=Path("."),
        )
        if result.returncode != 0:
            return [{
                "rule": "package_boundary",
                "file": "backend/",
                "message": "Package boundary violations detected. Run `python benchmarks/package_boundaries.py` for details.",
            }]
    except Exception as e:
        logger.debug(f"Could not run package_boundaries.py: {e}")
    return []


def run_governance_checks(check_core: bool = True, check_imports: bool = True,
                          check_boundaries: bool = True) -> dict:
    """Run all governance checks and return results."""
    results = {
        "passed": True,
        "violations": [],
    }

    all_violations = []

    # Get changed files for git-based checks
    changed_files = get_changed_files()

    if check_core:
        core_violations = check_core_changes(changed_files)
        all_violations.extend(core_violations)

    if check_imports:
        import_violations = check_cross_capability_imports(".")
        all_violations.extend(import_violations)

    if check_boundaries:
        boundary_violations = check_package_boundaries()
        all_violations.extend(boundary_violations)

    if all_violations:
        results["passed"] = False
        results["violations"] = all_violations

    return results


def main():
    parser = argparse.ArgumentParser(description="ECP Governance Enforcement")
    parser.add_argument("--check-core", action="store_true", default=True,
                        help="Check for unauthorized Core changes")
    parser.add_argument("--check-imports", action="store_true", default=True,
                        help="Check for cross-capability imports")
    parser.add_argument("--check-boundaries", action="store_true", default=True,
                        help="Check for package boundary violations")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    results = run_governance_checks(
        check_core=args.check_core,
        check_imports=args.check_imports,
        check_boundaries=args.check_boundaries,
    )

    if results["passed"]:
        logger.info("All governance checks passed!")
        return 0
    else:
        logger.error(f"Found {len(results['violations'])} governance violations:")
        for v in results["violations"]:
            logger.error(f"  [{v['rule']}] {v['message']}")
            if "file" in v:
                logger.error(f"    → {v['file']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
