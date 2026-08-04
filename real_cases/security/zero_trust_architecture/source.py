from flask import Flask, request

@app.route("/api/data")
def get_data():
    # No identity verification
    # No device posture check
    # No micro-segmentation
    return jsonify({"data": "sensitive_information"})

@app.route("/api/admin")
def admin():
    # No continuous verification
    # No least privilege
    return jsonify({"admin": "full_access"})

DATABASE_HOST = "10.0.1.50"
REDIS_HOST = "10.0.1.51"

# No zero trust controls
# No identity provider
# No policy engine

# Hardcoded credentials
API_KEY = "ztna_api_key_12345"