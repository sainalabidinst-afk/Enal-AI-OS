"""
Smoke tests for Society capability.
"""

import importlib


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    mod = importlib.import_module("apps.society")
    assert mod is not None


def test_capability_package() -> None:
    """Verify that capability package exists."""
    mod = importlib.import_module("apps.society.society")
    assert mod is not None


def test_society_modules_exist() -> None:
    """Verify that key society modules exist."""
    importlib.import_module("apps.society.agent")
    importlib.import_module("apps.society.conversation_manager")
    importlib.import_module("apps.society.executive")
    importlib.import_module("apps.society.intent_router")
    importlib.import_module("apps.society.society")
