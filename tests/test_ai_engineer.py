"""
Smoke tests for Ai Engineer capability.
"""

from apps.ai_engineer.agent_designer import *
from apps.ai_engineer.engine import *
from apps.ai_engineer.llmops_manager import *
from apps.ai_engineer.prompt_engineer import *
from apps.ai_engineer.rag_engine import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.ai_engineer")
    assert mod is not None
