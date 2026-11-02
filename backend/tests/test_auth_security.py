import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.app.core.config import AuthAccountSettings, Settings, settings
from backend.app.core.passwords import hash_password, verify_password
from backend.app.core.security_model import Permission, security_model
from backend.app.main import app, seed_default_security_policies

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


@pytest.mark.asyncio
async def test_startup_policy_grants_only_configured_permissions(monkeypatch):
    account = AuthAccountSettings(
        username="policy-test",
        password_hash=hash_password("test-password"),
        permissions=["read"],
    )
    monkeypatch.setattr(settings, "AUTH_ACCOUNT", account)

    await seed_default_security_policies()

    assert security_model.check_permission("policy-test", Permission.READ)
    assert not security_model.check_permission("policy-test", Permission.EXECUTE)


def test_settings_reject_weak_secret_and_missing_account_even_in_testing():
    with pytest.raises(ValidationError, match="SECRET_KEY must be a unique secret"):
        Settings(
            _env_file=None,
            SECRET_KEY="short",
            TESTING=True,
            AUTH_ACCOUNT={},
        )

    with pytest.raises(ValidationError, match="AUTH_ACCOUNT must define"):
        Settings(
            _env_file=None,
            SECRET_KEY="s" * 48,
            TESTING=True,
            AUTH_ACCOUNT={"username": "admin", "password_hash": "not-a-hash"},
        )


def test_settings_accept_valid_operator_configuration():
    account = {
        "username": "operator",
        "password_hash": hash_password("test-password"),
        "roles": ["admin"],
        "permissions": ["model:read", "read", "execute", "capabilities:execute"],
    }

    configured = Settings(
        _env_file=None,
        SECRET_KEY="s" * 48,
        TESTING=False,
        AUTH_ACCOUNT=account,
    )

    assert configured.AUTH_ACCOUNT.username == "operator"
    assert configured.AUTH_ACCOUNT.password_hash.get_secret_value() == account["password_hash"]
