"""
Package Boundary Enforcement
==============================

This module enforces dependency rules between ECP packages.

Allowed dependencies:
- apps → sdk
- apps → runtime
- sdk → kernel
- studio → runtime
- studio → kernel
- marketplace → runtime
- plugins → kernel
- runtime → kernel

Forbidden dependencies:
- kernel → runtime (kernel must not depend on runtime)
- kernel → sdk (kernel must not depend on sdk)
- runtime → apps (runtime must not depend on apps)
- sdk → runtime (SDK is client-side only)
"""

import ast
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# Define package boundaries
PACKAGE_BOUNDARIES = {
    "kernel": {
        "allowed": [],
        "forbidden": ["runtime", "sdk", "apps", "studio", "marketplace"],
    },
    "runtime": {
        "allowed": ["kernel"],
        "forbidden": ["apps", "sdk", "studio", "marketplace"],
    },
    "sdk": {
        "allowed": ["kernel"],
        "forbidden": ["runtime", "apps", "studio", "marketplace", "backend"],
    },
    "studio": {
        "allowed": ["runtime", "kernel"],
        "forbidden": ["apps", "sdk", "marketplace"],
    },
    "marketplace": {
        "allowed": ["runtime", "kernel"],
        "forbidden": ["apps", "sdk", "studio"],
    },
    "apps": {
        "allowed": ["sdk", "runtime"],
        "forbidden": ["kernel", "studio", "marketplace", "backend"],
    },
    "plugins": {
        "allowed": ["kernel"],
        "forbidden": ["runtime", "sdk", "apps", "studio", "marketplace", "backend"],
    },
}


def check_imports(file_path: str, package_name: str) -> list[str]:
    """Check if a file violates package boundaries."""
    violations = []
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
    except Exception as e:
        logger.debug(f"Could not parse {file_path}: {e}")
        return []

    package_rules = PACKAGE_BOUNDARIES.get(package_name, {})
    forbidden = package_rules.get("forbidden", [])

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for forbidden_pkg in forbidden:
                if module.startswith(forbidden_pkg):
                    violations.append(
                        f"{file_path}:{node.lineno}: import from '{module}' violates boundary "
                        f"({package_name} cannot import from {forbidden_pkg})"
                    )

    return violations


def check_package_boundaries(root_path: str) -> list[str]:
    """Check all packages for boundary violations."""
    violations = []
    root = Path(root_path)

    # Map directories to package names
    package_map = {
        "backend/app/core": "kernel",
        "backend/app/core/cognitive": "kernel",
        "backend/app/runtime": "runtime",
        "sdk": "sdk",
        "studio": "studio",
        "marketplace": "marketplace",
        "apps": "apps",
        "backend/app/plugins": "plugins",
    }

    for dir_path, package_name in package_map.items():
        full_path = root / dir_path
        if not full_path.exists():
            continue
        for py_file in full_path.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue
            violations.extend(check_imports(str(py_file), package_name))

    return violations


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    violations = check_package_boundaries(".")
    if violations:
        logger.error(f"Found {len(violations)} boundary violations:")
        for v in violations:
            logger.error(v)
        exit(1)
    else:
        logger.info("No package boundary violations found!")
