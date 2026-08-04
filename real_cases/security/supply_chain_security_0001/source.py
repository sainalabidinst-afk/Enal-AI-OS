def download_artifact(url):
    # No signature verification
    # No hash check
    urllib.request.urlretrieve(url, "/tmp/artifact.tar.gz")
    subprocess.run(["tar", "-xzf", "/tmp/artifact.tar.gz"])

# No provenance tracking
# No build security