import requests

def api_call():
    # HTTP instead of HTTPS
    return requests.get("http://api.example.com/data")

def database_connection():
    # No TLS
    conn = psycopg2.connect("postgresql://localhost/mydb")
    return conn

def internal_service():
    # No mTLS
    # Hardcoded credentials
    INTERNAL_KEY = "internal_key_12345"
    return requests.get("http://internal-service/api")