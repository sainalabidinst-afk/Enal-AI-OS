"""
Smoke tests for Documentation Engineer capability.
"""

from apps.documentation_engineer.architecture_docs import *
from apps.documentation_engineer.engine import *
from apps.documentation_engineer.openapi_generator import *
from apps.documentation_engineer.release_notes_generator import *
from apps.documentation_engineer.schemas import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.documentation_engineer")
    assert mod is not None
