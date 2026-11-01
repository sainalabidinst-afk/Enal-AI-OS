"""Regression tests for the canonical capability entrypoint contract."""

import pytest

from apps import APPS, list_apps
from apps.base import BaseReferenceApp
from apps.digital_twin_engine import DigitalTwinWorker


def test_all_registered_capabilities_expose_valid_entrypoints() -> None:
    """Every canonical capability must load as a concrete reference app."""
    assert len(APPS) >= 30
    assert {app["name"] for app in list_apps()} == set(APPS)

    for capability_id, registered_app in APPS.items():
        assert registered_app is not None, capability_id
        assert isinstance(registered_app, BaseReferenceApp), capability_id
        assert registered_app.name == capability_id
        assert callable(registered_app.run)


@pytest.mark.asyncio
async def test_digital_twin_worker_rejects_unknown_actions() -> None:
    worker = DigitalTwinWorker()

    with pytest.raises(ValueError, match="Unsupported digital twin action"):
        await worker.execute({"action": "unknown"})
