"""
Single Source of Truth for the Platform Version
===============================================

Resolves the platform version from, in order of precedence:

1. ``ECP_VERSION`` environment variable — explicit override (used by Docker
   images and release pipelines).
2. Installed distribution metadata for ``enal-backend``.
3. ``[project].version`` in ``pyproject.toml`` — source checkout.
4. :data:`FALLBACK_VERSION` — last resort so the backend can still boot.

Previously the version was hardcoded in three places that silently diverged:
``backend/app/core/config.py`` said ``3.0.0`` while ``pyproject.toml`` and the
``VERSION`` file said ``3.1.0-rc1``. ``/health`` and ``/`` reported ``3.0.0``
from a ``v3.1.0-rc1`` checkout. This module removes the duplicate declarations.
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from importlib import metadata
from pathlib import Path

logger = logging.getLogger(__name__)

DISTRIBUTION_NAME = "enal-backend"
FALLBACK_VERSION = "3.1.0rc1"


def _repo_root() -> Path:
    """Walk up from this file to the directory holding pyproject.toml."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    return Path(__file__).resolve().parents[4]


def _version_from_pyproject() -> str | None:
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
        return None
    pyproject = _repo_root() / "pyproject.toml"
    if not pyproject.is_file():
        return None
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        logger.warning("Could not parse pyproject.toml for version: %s", exc)
        return None
    version = data.get("project", {}).get("version")
    return str(version) if version else None


@lru_cache(maxsize=1)
def resolve_version() -> str:
    """Return the platform version string.

    Cached so the pyproject read and metadata lookup happen at most once.
    """
    override = os.environ.get("ECP_VERSION", "").strip()
    if override:
        return override

    try:
        return metadata.version(DISTRIBUTION_NAME)
    except metadata.PackageNotFoundError:
        pass

    from_pyproject = _version_from_pyproject()
    if from_pyproject:
        return from_pyproject

    logger.warning(
        "Could not resolve platform version from ECP_VERSION, %s metadata, or "
        "pyproject.toml; falling back to %s",
        DISTRIBUTION_NAME,
        FALLBACK_VERSION,
    )
    return FALLBACK_VERSION


def reset_version_cache() -> None:
    """Clear the memoized version. Intended for tests and hot reload."""
    resolve_version.cache_clear()


__all__ = [
    "DISTRIBUTION_NAME",
    "FALLBACK_VERSION",
    "reset_version_cache",
    "resolve_version",
]
