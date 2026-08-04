def transfer_funds(from_id, to_id, amount):
    from_query = f"UPDATE accounts SET balance = balance - {amount} WHERE id = {from_id}"
    to_query = f"UPDATE accounts SET balance = balance + {amount} WHERE id = {to_id}"
    cursor.execute(from_query)
    cursor.execute(to_query)
    return True

def modify_permissions(user_id, permissions):
    user = User.query.get(user_id)
    user.permissions = permissions
    db.commit()

@app.route("/api/admin/config")
def admin_config():
    return jsonify({"config": "admin_secrets"})