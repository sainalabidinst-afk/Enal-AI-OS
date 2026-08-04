@app.route("/api/users/<int:user_id>")
def get_user_data(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.to_dict())

@app.route("/api/users/<int:user_id>/email")
def get_user_email(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify({"email": user.email})

@app.route("/api/users/<int:user_id>/ssn")
def get_user_ssn(user_id):
    user = User.query.filter_by(id=user_id).first()
    query = f"SELECT ssn FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return jsonify({"ssn": result[0]})