import pytest

from apps import APPS


@pytest.mark.parametrize(
    "pack_name",
    [
        "ai-ethics-governance",
        "supply-chain-analyst",
        "data-scientist",
        "business-intelligence",
        "innovation-strategist",
        "devsecops",
    ],
)
def test_new_pack_is_registered_with_worker(pack_name: str) -> None:
    app = APPS.get(pack_name)

    assert app is not None
    assert app.name == pack_name
    assert callable(app.worker.execute)
