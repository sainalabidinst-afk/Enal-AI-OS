import os

import pytest

from backend.app.core.platform_version import resolve_version

os.environ.setdefault("SECRET_KEY", "test-secret")


def test_settings_defaults():
    from backend.app.core.config import Settings

    settings = Settings()
    assert settings.PROJECT_NAME == "Enal AI OS"
    assert settings.VERSION == resolve_version()
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DEFAULT_MODEL == "ollama/llama3:8b"
    assert settings.MAX_TOKENS == 8192
    assert settings.TEMPERATURE == 0.7


def test_require_database_url_raises_when_empty():
    from backend.app.core.config import Settings

    settings = Settings(DATABASE_URL="", SECRET_KEY="test")
    with pytest.raises(ValueError):
        settings.require_database_url()


def test_require_database_url_returns_value():
    from backend.app.core.config import Settings

    settings = Settings(DATABASE_URL="sqlite:///:memory:", SECRET_KEY="test")
    assert settings.require_database_url() == "sqlite:///:memory:"
