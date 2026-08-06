def get_user(user_id):
    if user_id == 1:
        return {"role": "admin"}
    return {"role": "user"}

@app.route("/api/users/<int:user_id>")
def user_endpoint(user_id):
    user = get_user(user_id)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return jsonify(user)

@app.route("/api/admin")
def admin():
    if request.user.role == "admin":
        return jsonify({"admin_data": "secret"})

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    query = f"DELETE FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return jsonify({"status": "deleted"})