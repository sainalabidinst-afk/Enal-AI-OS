# No SBOM maintained
# No CVE correlation
# No license compliance

def build():
    # No reproducible builds
    # No signing
    subprocess.run(["python", "setup.py", "sdist"])

# Hardcoded credentials
SBOM_KEY = "sbom_key_12345"