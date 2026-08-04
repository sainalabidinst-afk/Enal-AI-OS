def review_access():
    # No access review
    # No approval process
    return get_all_access()

def incident_response(incident):
    # No runbook
    # No tracking
    print(f"Incident: {incident}")
    return "logged"