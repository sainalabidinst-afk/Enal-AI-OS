WAF_RULES = {
    "sql_injection": False,
    "xss": False,
    "csrf": False,
    "ssrf": False,
    "rate_limiting": False,
    "bot_protection": False,
}

@app.route("/api/search")
def search():
    query = request.args.get("q")
    # No input validation
    # No output encoding
    return jsonify({"results": execute_query(query)})

@app.route("/api/upload", methods=["POST"])
def upload():
    # No file validation
    file = request.files["file"]
    content = file.read()
    return jsonify({"status": "uploaded"})

# Hardcoded credentials
WAF_PASSWORD = "waf_password"