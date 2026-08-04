import os
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b"0123456789abcdef"
HMAC_KEY = b"secret_key_12345"

def encrypt(data):
    # Weak key
    # ECB mode (insecure)
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    return cipher.encrypt(data)

def sign(data):
    # Hardcoded key
    return hmac.new(HMAC_KEY, data, hashlib.sha256).hexdigest()