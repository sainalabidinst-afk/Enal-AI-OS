import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.app.core.config import AuthAccountSettings, Settings, settings
from backend.app.core.passwords import hash_password, verify_password
from backend.app.main import app

client = TestClient(app)


def test_scrypt_password_hash_verifies_password():
    encoded = hash_password("strong-test-password")

    assert verify_password("strong-test-password", encoded)
    assert not verify_password("incorrect-password", encoded)
    assert not verify_password("password", "invalid-hash")


def test_login_issues_only_configured_identity_and_permissions():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test", "password": "test"},
    )

    assert response.status_code == 200
    data = response.json()
    payload = jwt.decode(data["access_token"], settings.SECRET_KEY, algorithms=["HS256"])
    assert payload["sub"] == "test"
    assert payload["permissions"] == settings.AUTH_ACCOUNT.permissions
    assert data["expires_in"] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


@pytest.mark.parametrize(
    ("username", "password"),
    [("test", "wrong-password"), ("unknown-user", "test")],
)
def test_login_rejects_invalid_credentials_generically(username: str, password: str):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password."


def test_login_fails_closed_without_configured_account(monkeypatch):
    monkeypatch.setattr(settings, "AUTH_ACCOUNT", AuthAccountSettings())

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test", "password": "test"},
    )

    assert response.status_code == 503


def test_token_with_revoked_permission_is_rejected(monkeypatch):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test", "password": "test"},
    )
    token = response.json()["access_token"]
    monkeypatch.setattr(
        settings,
        "AUTH_ACCOUNT",
        settings.AUTH_ACCOUNT.model_copy(update={"permissions": ["model:read", "read"]}),
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_production_settings_reject_weak_secret_and_missing_account():
    with pytest.raises(ValidationError, match="SECRET_KEY must be a unique secret"):
        Settings(
            _env_file=None,
            SECRET_KEY="short",
            TESTING=False,
            AUTH_ACCOUNT={},
        )

    with pytest.raises(ValidationError, match="AUTH_ACCOUNT must define"):
        Settings(
            _env_file=None,
            SECRET_KEY="s" * 48,
            TESTING=False,
            AUTH_ACCOUNT={"username": "admin", "password_hash": "not-a-hash"},
        )
