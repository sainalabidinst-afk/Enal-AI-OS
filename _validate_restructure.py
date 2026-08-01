#!/usr/bin/env python3
"""Validate that the monorepo restructure is working."""

import sys


def _encode_safe(text: str) -> str:
    """Replace characters that may not be encodable in the active console codepage."""
    return (
        text.replace("\u2705", "[OK]")
        .replace("\u274c", "[FAIL]")
        .replace("\u2014", "-")
        .replace("\u2714", "[OK]")
    )


def validate_import(module_path: str) -> bool:
    try:
        __import__(module_path)
        print(_encode_safe(f"  [OK] import {module_path} - PASS"))
        return True
    except Exception as e:
        print(_encode_safe(f"  [FAIL] import {module_path} - FAIL: {e}"))
        return False


def main():
    print("\n" + "=" * 60)
    print("  Monorepo Restructure Validation")
    print("=" * 60 + "\n")

    all_pass = True

    # Module-level imports
    checks = [
        ("backend", "backend"),
        ("backend.app", "backend.app"),
        ("backend.app.main", "backend.app.main"),
        ("apps", "apps"),
        ("plugins", "plugins"),
        ("workspace", "workspace"),
    ]

    for name, path in checks:
        result = validate_import(path)
        if not result:
            all_pass = False

    # Direct from-import
    try:
        from backend.app.main import app
        print(_encode_safe("  [OK] from backend.app.main import app - PASS"))
    except Exception as e:
        print(_encode_safe(f"  [FAIL] from backend.app.main import app - FAIL: {e}"))
        all_pass = False

    print()
    if all_pass:
        print("  [OK] ALL CHECKS PASSED")
    else:
        print("  [FAIL] SOME CHECKS FAILED")
    print("=" * 60 + "\n")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())

