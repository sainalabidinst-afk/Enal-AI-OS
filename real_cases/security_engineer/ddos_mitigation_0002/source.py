@app.route("/api/upload", methods=["POST"])
def upload():
    # No file size limit
    # No content type validation
    file = request.files["file"]
    content = file.read()
    # Hardcoded credentials
    UPLOAD_KEY = "upload_key_12345"
    return jsonify({"size": len(content)})