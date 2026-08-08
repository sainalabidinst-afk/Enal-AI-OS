import os

import pytest

os.environ.setdefault("SECRET_KEY", "test-secret")


def test_settings_defaults():
    from backend.app.core.config import Settings

    settings = Settings()
    assert settings.PROJECT_NAME == "Enal AI OS"
    assert settings.VERSION == "1.0.0-dev"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DEFAULT_MODEL == "gpt-4o"
    assert settings.MAX_TOKENS == 4096
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
