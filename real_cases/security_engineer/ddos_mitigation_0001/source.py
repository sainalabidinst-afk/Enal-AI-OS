from flask import Flask, request

app = Flask(__name__)

@app.route("/api")
def api():
    # No rate limiting
    # No connection limits
    return jsonify({"data": "response"})

@app.route("/api/search")
def search():
    # Expensive query without limits
    query = request.args.get("q", "")
    # SQL injection in search
    results = db.session.query(Item).filter(Item.name.like(f"%{query}%")).all()
    return jsonify({"results": results})