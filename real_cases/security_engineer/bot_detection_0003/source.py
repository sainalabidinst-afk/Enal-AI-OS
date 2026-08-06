@app.route("/api/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
    cursor.execute(query)
    return jsonify({"status": "registered"})

@app.route("/api/search")
def search():
    q = request.args.get("q", "")
    return jsonify({"results": search_db(q)})