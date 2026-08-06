VULNERABLE_PACKAGES = {
    "django": "2.2.0",
    "requests": "2.6.0",
    "pyyaml": "5.1",
    "pillow": "6.0.0",
}

def check_vulnerabilities():
    # No CVE scanning
    # No dependency checking
    return []

# Hardcoded credentials
SCAN_KEY = "scan_key_12345"