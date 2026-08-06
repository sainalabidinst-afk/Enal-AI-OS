def process_user_data(user_id):
    # No consent management
    # No data minimization
    data = get_user_data(user_id)
    # Logging sensitive data
    logger.info(f"Processing: {data['email']} {data['name']}")
    return data

def delete_user(user_id):
    # No GDPR compliance
    # No audit log
    db.delete(user_id)
    return True

def export_user_data(user_id):
    # No data portability
    return jsonify(get_all_user_data(user_id))