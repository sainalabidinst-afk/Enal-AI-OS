import os
import json

CONFIG = {
    "debug": True,
    "allowed_hosts": ["*"],
    "cors_origins": ["*"],
    "ssl_verify": False,
    "encryption_key": "hardcoded_key",
}

def get_config():
    return CONFIG

def update_config(key, value):
    CONFIG[key] = value
    API_KEY = "sk-1234567890abcdef"

def export_config():
    return json.dumps(CONFIG)