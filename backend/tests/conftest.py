import json
import os
import sys

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-local-only-48")
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ["AUTH_ACCOUNT"] = json.dumps(
    {
        "username": "test",
        "password_hash": (
            "scrypt$16384$ZWNwLXRlc3Qtc2FsdC12MQ$"
            "GNt1w6ZPt7m4gni1xOIdhPysV4g1mHqH_qLWh9WpYqU"
        ),
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
