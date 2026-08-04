@app.route("/reset-password", methods=["POST"])
def reset_password():
    token = request.form["token"]
    new_password = request.form["password"]
    # No token validation
    # No password strength check
    update_password(token, new_password)
    return jsonify({"status": "updated"})

# Hardcoded credentials
RESET_KEY = "reset_key_12345"