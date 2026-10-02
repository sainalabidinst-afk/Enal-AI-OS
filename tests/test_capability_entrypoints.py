"""Regression tests for the canonical capability entrypoint contract."""

from apps import APPS
from apps.base import BaseReferenceApp


def test_all_registered_capabilities_expose_valid_entrypoints() -> None:
    """Every canonical capability must load as a concrete reference app."""
    assert len(APPS) >= 30

    for capability_id, registered_app in APPS.items():
        assert registered_app is not None, capability_id
        assert isinstance(registered_app, BaseReferenceApp), capability_id
        assert registered_app.name == capability_id
        assert callable(registered_app.run)
