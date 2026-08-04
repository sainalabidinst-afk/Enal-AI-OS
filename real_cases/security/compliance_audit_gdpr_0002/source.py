def store_personal_data(user_id, data):
    # No consent
    # No encryption
    db.insert("personal_data", {"user": user_id, "data": data})

def share_data_with_thirdparty(user_id, recipient):
    # No DPA
    # No encryption in transit
    send_email(recipient, get_personal_data(user_id))