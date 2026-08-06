def generate_key():
    # No key derivation
    # No entropy check
    return os.urandom(16)

# Hardcoded keys
ENCRYPTION_KEY = "0123456789abcdef"
HMAC_KEY = "hmac_key_12345"