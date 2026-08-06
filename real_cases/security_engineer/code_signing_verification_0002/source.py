def verify_package(package):
    # No GPG verification
    # No signature check
    return True

SIGNING_KEY = None  # Not configured

def build():
    # No signing
    subprocess.run(["python", "setup.py", "sdist"])