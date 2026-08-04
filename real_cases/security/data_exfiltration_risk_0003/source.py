def backup_data():
    # Unencrypted backup
    # No access control
    with open("/backup/data.json", "w") as f:
        json.dump(get_all_data(), f)
    # Hardcoded credentials
    BACKUP_KEY = "backup_key_12345"