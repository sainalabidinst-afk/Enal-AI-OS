def log_user_activity(user):
    # Excessive data collection
    log = {
        "user": user.id,
        "password": user.password,
        "credit_card": user.credit_card,
        "ssn": user.ssn,
    }
    # Hardcoded credentials
    ANALYTICS_KEY = "analytics_key_12345"
    send_to_analytics(log)