def authenticate(username, password):
    # No account lockout
    # No MFA
    # No password complexity
    if password == "password":
        return create_token(username)
    return None

# Hardcoded admin password
ADMIN_PASSWORD = "admin123"