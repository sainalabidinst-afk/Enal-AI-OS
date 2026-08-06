import urllib.request
import subprocess
import hashlib

def install_package(package):
    # Downloading from untrusted source
    # No signature verification
    url = f"https://pypi.org/packages/{package}.tar.gz"
    urllib.request.urlretrieve(url, f"/tmp/{package}.tar.gz")
    subprocess.run(["tar", "-xzf", f"/tmp/{package}.tar.gz"])
    subprocess.run(["python", "setup.py", "install"])

def build_artifact():
    # No reproducible builds
    # No signing
    subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"])
    return "dist/"

def verify_checksum(file_path, expected_hash):
    # Weak hash algorithm
    return hashlib.md5(open(file_path, "rb").read()).hexdigest() == expected_hash