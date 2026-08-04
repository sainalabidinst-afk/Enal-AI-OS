import ssl
import yaml

def load_config(path):
    # Unsafe YAML loading
    config = yaml.load(f)
    return config

def connect_ssl():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context