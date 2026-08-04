import socket
import ssl
import requests

def connect_insecure(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def weak_ssl_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def disable_cert_validation():
    requests.packages.urllib3.disable_warnings()
    return requests.get("https://example.com", verify=False)