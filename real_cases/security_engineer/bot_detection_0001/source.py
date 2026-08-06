from flask import Flask, request
import jwt

app = Flask(__name__)

@app.route("/api/data")
def get_data():
    # No bot detection
    query = request.args.get("q", "")
    return jsonify({"results": search(query)})

@app.route("/api/form", methods=["POST"])
def submit_form():
    # No CSRF token
    return jsonify({"status": "submitted"})

@app.route("/api/scrape")
def scrape():
    url = request.args.get("url")
    return requests.get(url).content