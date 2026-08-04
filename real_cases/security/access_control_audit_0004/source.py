@app.route("/api/posts/<post_id>")
def get_post(post_id):
    post = Post.query.get(post_id)
    return jsonify({"title": post.title, "content": post.content})

@app.route("/api/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    query = f"DELETE FROM posts WHERE id = {post_id}"
    cursor.execute(query)
    db.delete(post)
    db.commit()

@app.route("/api/users/<user_id>/data")
def user_data(user_id):
    data = get_user_data(user_id)
    return jsonify(data)