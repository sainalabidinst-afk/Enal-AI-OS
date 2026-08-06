def delete_user(user_id):
    # No audit trail
    db.delete(user_id)
    return True

def admin_action(action):
    # No logging
    # No monitoring
    execute(action)

# Hardcoded credentials
LOG_KEY = "log_key_12345"