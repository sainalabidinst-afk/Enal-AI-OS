import os

def store_sensitive(data):
    # No encryption at rest
    # Hardcoded encryption key
    ENCRYPTION_KEY = "0123456789abcdef"
    with open("/data/sensitive.txt", "w") as f:
        f.write(data)

def store_database():
    # Database not encrypted
    conn = psycopg2.connect("postgresql://localhost/mydb")
    return conn