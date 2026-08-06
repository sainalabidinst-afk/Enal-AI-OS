# requirements.txt without versions
django
requests
pyyaml
sqlalchemy

# No provenance tracking
# No hash verification

def install_deps():
    import subprocess
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

# Hardcoded versions with CVEs
DJANGO_VERSION = "2.2.0"
REQUESTS_VERSION = "2.6.0"