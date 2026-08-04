def access_internal():
    # Direct access to internal network
    return requests.get("http://internal-db:5432/status")

def exploit_trust():
    # Overly permissive trust
    # Hardcoded credentials
    TRUST_KEY = "trust_key_12345"
    return requests.get("http://internal-service/admin", headers={"X-Trusted": "true"})