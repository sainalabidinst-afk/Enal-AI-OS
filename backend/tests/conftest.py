import base64
import hashlib
import json
import os
import secrets
import sys

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-local-only-48")
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def _test_password_hash() -> str:
    def encode(value: bytes) -> str:
        return base64.urlsafe_b64encode(value).decode().rstrip("=")

    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        b"test",
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=32,
    )
    return f"scrypt:16384:{encode(salt)}:{encode(digest)}"


os.environ["AUTH_ACCOUNT"] = json.dumps(
    {
        "username": "test",
        "password_hash": _test_password_hash(),
        "roles": ["default"],
        "permissions": [
            "model:read",
            "capabilities:execute",
            "read",
            "write",
            "execute",
        ],
    }
)
