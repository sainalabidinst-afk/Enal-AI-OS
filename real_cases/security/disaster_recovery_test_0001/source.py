import os
import shutil

BACKUP_CONFIG = {
    "enabled": False,
    "frequency": "never",
    "retention": "0 days",
    "encryption": False,
    "offsite": False,
}

def backup():
    # No automated backup
    shutil.copytree("/data", "/backup")
    return True

def restore():
    # No tested restore procedure
    return False

# Hardcoded credentials
DB_PASSWORD = "backup_password123"