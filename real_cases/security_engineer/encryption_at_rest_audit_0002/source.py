def save_file(filename, content):
    # No encryption
    # No access control
    # Hardcoded key
    ENCRYPTION_KEY = "encryption_key_12345"
    with open(f"/storage/{filename}", "wb") as f:
        f.write(content)