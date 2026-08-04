INCIDENT_RESPONSE = {
    "automated": False,
    "playbooks": [],
    "integration": {"siem": None, "firewall": None}
}

def handle_incident(incident):
    # Manual process
    # No containment
    print(f"Incident: {incident}")
    return "logged"