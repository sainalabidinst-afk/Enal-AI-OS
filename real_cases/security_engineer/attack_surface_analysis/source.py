@app.route("/api/v1/users/<int:user_id>", methods=["GET", "POST", "PUT", "DELETE"])
def user_api(user_id):
    if request.method == "GET":
        query = f"SELECT * FROM users WHERE id = {user_id}"
        cursor.execute(query)
        return jsonify(cursor.fetchone())
    elif request.method == "POST":
        return create_user(request.json)
    elif request.method == "PUT":
        data = request.json
        query = f"UPDATE users SET name = '{data['name']}' WHERE id = {user_id}"
        cursor.execute(query)
        return jsonify({"status": "updated"})
    elif request.method == "DELETE":
        query = f"DELETE FROM users WHERE id = {user_id}"
        cursor.execute(query)
        return jsonify({"status": "deleted"})