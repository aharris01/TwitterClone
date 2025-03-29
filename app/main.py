from flask import request, jsonify
from config import app
from markupsafe import escape


@app.route("/<name>")
def hello(name):
    return f"Hello, {name}!"


@app.route("/<int:post_id>")
def show_post(post_id):
    return f"Post {post_id}"


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)
