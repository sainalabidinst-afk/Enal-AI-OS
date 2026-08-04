def get_secrets():
    # Secrets in plain text
    # No KMS encryption
    return {"key": "plaintext_secret", "password": "MyP@ssw0rd123"}

def create_db():
    # No encryption at rest
    # Publicly accessible
    rds.create_db_instance(PubliclyAccessible=True, StorageEncrypted=False)