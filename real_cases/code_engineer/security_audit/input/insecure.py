"""
Security Audit Example
=======================

Code with various security vulnerabilities for audit analysis.
"""

import os
import pickle
import subprocess
from typing import Any

# Hardcoded credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "SuperSecret123!"
JWT_SECRET = "my-secret-key"

# Insecure deserialization
def load_config(config_path: str) -> Any:
    """Load config from pickle file - unsafe deserialization."""
    with open(config_path, "rb") as f:
        return pickle.loads(f.read())


# Command injection
def run_backup(database: str, output_path: str) -> None:
    """Run database backup - command injection vulnerability."""
    cmd = f"pg_dump {database} > {output_path}"
    os.system(cmd)


# Path traversal
def read_user_file(username: str, filename: str) -> str:
    """Read user file - path traversal vulnerability."""
    base_path = f"/home/{username}/files/"
    file_path = base_path + filename
    with open(file_path, "r") as f:
        return f.read()


# Weak cryptography
import hashlib

def hash_password(password: str) -> str:
    """Hash password using MD5 - cryptographically broken."""
    return hashlib.md5(password.encode()).hexdigest()


# SSRF vulnerability
import requests

def fetch_external_data(url: str) -> str:
    """Fetch external data - SSRF vulnerability."""
    response = requests.get(url)
    return response.text


# Debug mode in production
DEBUG = True
SECRET_KEY = "debug-secret-key"


# Insecure CORS
CORS_ORIGINS = ["*"]


# Verbose error handling
def process_order(order_id: str) -> dict:
    """Process order with verbose error handling."""
    try:
        # Process order logic
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e), "traceback": str(e.__traceback__)}
