@app.route("/api/data")
def get_data():
    # No WAF
    # No rate limiting
    # No bot detection
    query = request.args.get("q", "")
    return jsonify({"results": search(query)})

# Hardcoded WAF credentials
WAF_PASSWORD = "waf_password"