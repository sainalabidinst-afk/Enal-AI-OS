@app.route("/api/users/<int:user_id>")
def user_profile(user_id):
    user = get_user(user_id)
    query = f"SELECT * FROM profiles WHERE user_id = {user_id}"
    cursor.execute(query)
    return jsonify(user)

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    query = f"UPDATE users SET name = '{data['name']}' WHERE id = {user_id}"
    cursor.execute(query)
    return jsonify({"status": "updated"})

@app.route("/api/documents/<doc_id>")
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return doc.content