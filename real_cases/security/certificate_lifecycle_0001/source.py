import ssl
import requests

def check_cert():
    # No expiration check
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return requests.get("https://api.example.com", verify=False)

def make_request():
    # No certificate validation
    return requests.get("https://api.example.com", verify=False)