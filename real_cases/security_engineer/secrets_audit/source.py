import os

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "SuperSecret123!"
API_KEY = "sk-1234567890abcdefghij"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGcY5unA67hqlFvN
-----END RSA PRIVATE KEY-----"""

def connect_db():
    password = "MyP@ssw0rd!"
    conn = psycopg2.connect(host="localhost", database="mydb", user="admin", password=password)
    return conn

GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"