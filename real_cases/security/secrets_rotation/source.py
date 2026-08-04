LEGACY_API_KEY = "old_key_12345"
NEW_API_KEY = "new_key_67890"

def old_service():
    return requests.get("https://api.old.com/v1", headers={"Authorization": "Bearer old_key_12345"})

def new_service():
    return requests.get("https://api.new.com/v1", headers={"Authorization": "Bearer new_key_67890"})

DB_PASS = "P@ssword1"
DB_PASS_2 = "P@ssword1"
DB_PASSWORD = "P@ssword1"

AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# No key rotation
# No secrets manager