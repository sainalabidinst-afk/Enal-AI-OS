import os
import sys

# Ensure backend package is importable from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Set required environment variables for tests
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
