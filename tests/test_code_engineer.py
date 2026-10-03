"""
Smoke tests for Code Engineer capability.
"""

from apps.code_engineer.analyzer import *  # noqa: F403
from apps.code_engineer.architecture_models import *  # noqa: F403
from apps.code_engineer.architecture_patterns import *  # noqa: F403
from apps.code_engineer.architecture_reader import *  # noqa: F403
from apps.code_engineer.clean_architecture import *  # noqa: F403


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.code_engineer")
    assert mod is not None
