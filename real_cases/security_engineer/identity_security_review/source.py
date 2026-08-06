from flask import Flask, request, session
import jwt

app = Flask(__name__)
app.secret_key = "hardcoded_secret_12345"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # No rate limiting
    # No MFA
    session["user"] = username
    session["role"] = "admin"
    return jsonify({"status": "logged in"})

def verify_token(token):
    # No algorithm verification
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded

# Hardcoded secret
JWT_SECRET = "super_secret_key"