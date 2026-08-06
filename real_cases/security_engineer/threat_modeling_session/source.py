ARCHITECTURE = """
Web application with:
- Frontend: React SPA
- API Gateway: Kong
- User Service: Python/Flask
- Database: PostgreSQL
- Cache: Redis
- External APIs: Payment gateway
"""

COMPONENTS = ["API Gateway", "User Service", "Database", "Cache"]
DATA_FLOWS = [{"from": "User", "to": "API"}, {"from": "API", "to": "Database"}]

# No STRIDE analysis
# No threat catalog
# No risk assessment

# Hardcoded database credentials
DB_PASSWORD = "threat_model_password"