import base64
import binascii
import hashlib
import hmac
import secrets
from getpass import getpass

SCRYPT_N = 16384
SCRYPT_R = 8
SCRYPT_P = 1
SALT_LENGTH = 16
KEY_LENGTH = 32


def _decode_password_hash(encoded: str) -> tuple[bytes, bytes] | None:
    try:
        algorithm, cost, salt, digest = encoded.split(":")
        salt_bytes = base64.b64decode(
            salt + "=" * (-len(salt) % 4),
            altchars=b"-_",
            validate=True,
        )
        digest_bytes = base64.b64decode(
            digest + "=" * (-len(digest) % 4),
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, binascii.Error):
        return None

    if (
        algorithm != "scrypt"
        or cost != str(SCRYPT_N)
        or len(salt_bytes) != SALT_LENGTH
        or len(digest_bytes) != KEY_LENGTH
    ):
        return None
    return salt_bytes, digest_bytes


def is_password_hash(encoded: str) -> bool:
    """Return whether an encoded password hash uses the supported scrypt format."""
    return _decode_password_hash(encoded) is not None


def hash_password(password: str) -> str:
    """Hash a password with scrypt and a cryptographically random salt."""
    salt = secrets.token_bytes(SALT_LENGTH)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=KEY_LENGTH,
    )
    salt_encoded = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    digest_encoded = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"scrypt:{SCRYPT_N}:{salt_encoded}:{digest_encoded}"


def verify_password(password: str, encoded: str) -> bool:
    """Check a password against the supported scrypt hash format."""
    parsed = _decode_password_hash(encoded)
    if parsed is None:
        return False

    salt, expected_digest = parsed
    actual_digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=KEY_LENGTH,
    )
    return hmac.compare_digest(actual_digest, expected_digest)


if __name__ == "__main__":
    print(hash_password(getpass("Password to hash: ")))
