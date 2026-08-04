def store_health_data(patient_id, data):
    # No HIPAA compliance
    # No encryption at rest
    db.insert("health_data", {"patient": patient_id, "data": data})

def access_phi(user_id):
    # No audit trail
    # No minimum necessary
    return get_phi(user_id)

def share_phi(patient_id, recipient):
    # No BAA
    # No encryption in transit
    send_email(recipient, get_phi(patient_id))