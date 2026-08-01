#!/usr/bin/env python3
"""Diagnostic script — writes UTF-8 report to _diag_report.txt to avoid Windows cp1252 issues."""
import sys
import importlib
from pathlib import Path

lines: list[str] = []


def log(msg: str) -> None:
    lines.append(msg)


def check_import(name: str) -> None:
    try:
        importlib.import_module(name)
        log(f"IMPORT {name}: PASS")
    except Exception as e:
        log(f"IMPORT {name}: FAIL - {type(e).__name__}: {e}")


def check_pkg(name: str) -> None:
    try:
        mod = importlib.import_module(name)
        ver = getattr(mod, "__version__", "?")
        log(f"PKG {name}: {ver}")
    except Exception as e:
        log(f"PKG {name}: MISSING - {type(e).__name__}: {e}")


log("=" * 50)
log("IMPORT CHECKS")
log("=" * 50)
check_import("backend")
check_import("backend.app")
check_import("backend.app.main")

try:
    from backend.app.main import app
    log("FROM backend.app.main import app: PASS")
except Exception as e:
    log(f"FROM backend.app.main import app: FAIL - {type(e).__name__}: {e}")

check_import("apps")
check_import("plugins")
check_import("workspace")

log("")
log("=" * 50)
log("KEY PACKAGES")
log("=" * 50)
for pkg in [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "pydantic",
    "pydantic_settings",
    "litellm",
    "httpx",
    "redis",
    "qdrant_client",
    "aiohttp",
    "pytest",
    "pytest_asyncio",
]:
    check_pkg(pkg)

log("")
log(f"PYTHON EXE: {sys.executable}")
log(f"PYTHON VERSION: {sys.version}")

Path("_diag_report.txt").write_text("\n".join(lines), encoding="utf-8")
print("Diag report written to _diag_report.txt")

