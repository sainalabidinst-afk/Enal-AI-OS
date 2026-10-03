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
from typing import Any

logger = logging.getLogger(__name__)


# Define package boundaries
PACKAGE_BOUNDARIES = {
    "kernel": {
        "allowed": [],
        "forbidden": ["runtime", "sdk", "apps", "studio", "marketplace", "backend.app.runtime"],
    },
    "runtime": {
        "allowed": ["kernel"],
        "forbidden": ["apps", "studio", "marketplace"],
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
        "allowed": ["sdk", "runtime", "backend.app.runtime"],
        "forbidden": ["backend.app.core", "kernel", "studio", "marketplace"],
    },
    "plugins": {
        "allowed": ["kernel", "runtime"],
        "forbidden": ["sdk", "apps", "studio", "marketplace"],
    },
}


def check_imports(file_path: str, package_name: str) -> list[str]:
    """Check if a file violate package boundaries."""
    violations = []
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
    except Exception as e:
        logger.debug(f"Could not parse {file_path}: {e}")
        return []

    package_rules = PACKAGE_BOUNDARIES.get(package_name, {})
    forbidden = package_rules.get("forbidden", [])
    Path(file_path)

    file_str = str(file_path).replace("\\", "/")
    own_package_prefix = None
    if file_str.startswith("backend/app/core/"):
        own_package_prefix = "backend.app.core"
    elif file_str.startswith("backend/app/core/cognitive/"):
        own_package_prefix = "backend.app.core.cognitive"
    elif file_str.startswith("backend/app/runtime/"):
        own_package_prefix = "backend.app.runtime"
    elif file_str.startswith("backend/app/models/"):
        own_package_prefix = "backend.app.models"
    elif file_str.startswith("backend/app/api/"):
        own_package_prefix = "backend.app.api"
    elif file_str.startswith("backend/app/plugins/"):
        own_package_prefix = "backend.app.plugins"

    # Collect top-level imports (module scope) for boundary checking.
    # Lazy imports inside functions are exempt — they are used for
    # dynamic loading and avoid circular dependencies.
    top_level_imports: list[tuple[Any, str]] = []  # (node, module_or_name)

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_level_imports.append((node, alias.name))
            else:
                top_level_imports.append((node, node.module or ""))

    for node, module in top_level_imports:
        # Skip if importing from own package (intra-package)
        if own_package_prefix and (
            module == own_package_prefix or module.startswith(own_package_prefix + ".")
        ):
            continue

        # For function-level imports (lazy), the node won't be in top_level_imports
        # so they are already excluded.

        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                for forbidden_pkg in forbidden:
                    if module == forbidden_pkg or module.startswith(forbidden_pkg + "."):
                        violations.append(
                            f"{file_path}:{node.lineno}: import '{module}' violates boundary "
                            f"({package_name} cannot import from {forbidden_pkg})"
                        )

        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for forbidden_pkg in forbidden:
                if module == forbidden_pkg or module.startswith(forbidden_pkg + "."):
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
