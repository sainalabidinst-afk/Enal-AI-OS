INCIDENT_RESPONSE = {
    "detection_time": "manual",
    "response_time": "24 hours",
    "escalation": "email",
    "containment": "manual",
    "recovery": "manual",
}

# No runbooks
# No playbooks

def detect_incident():
    # No automated detection
    return False

# Hardcoded credentials
IR_PASSWORD = "incident_response_password"