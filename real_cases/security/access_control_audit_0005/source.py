@app.route("/api/admin/users")
def list_users():
    return jsonify(get_all_users())

@app.route("/api/admin/logs")
def admin_logs():
    return jsonify(get_logs())

@app.route("/api/admin/settings")
def admin_settings():
    return jsonify(get_settings())

def change_password(user_id, new_password):
    query = f"UPDATE users SET password = '{new_password}' WHERE id = {user_id}"
    cursor.execute(query)