"""
Generate smoke tests for capabilities that are missing test files.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = ROOT / "tests"
APPS_DIR = ROOT / "apps"

CAPABILITIES = [
    "ai_engineer",
    "business_analyst",
    "code_engineer",
    "data_engineer",
    "database_engineer",
    "devops_assistant",
    "documentation_engineer",
    "full_stack_engineer",
    "infrastructure_engineer",
    "network_engineer",
    "product_manager",
    "qa_engineer",
    "self_development",
    "system_architect",
    "ui_ux_designer",
]


def get_capability_modules(name: str) -> list[str]:
    app_dir = APPS_DIR / name
    if not app_dir.exists():
        return []
    py_files = [p.stem for p in app_dir.glob("*.py") if p.name != "__init__.py"]
    return py_files


def generate_test(name: str) -> str:
    modules = get_capability_modules(name)
    imports = "\n".join(f"from apps.{name}.{m} import *" for m in modules[:5])
    if not imports:
        imports = f"from apps.{name} import *"

    content = f'''"""
Smoke tests for {name.replace("_", " ").title()} capability.
"""

{imports}


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.{name}")
    assert mod is not None
'''
    return content


def main() -> int:
    created = 0
    for capability in CAPABILITIES:
        test_file = TESTS_DIR / f"test_{capability}.py"
        if test_file.exists():
            continue
        content = generate_test(capability)
        test_file.write_text(content, encoding="utf-8")
        print(f"Created: {test_file}")
        created += 1
    print(f"\nCreated {created} test files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
