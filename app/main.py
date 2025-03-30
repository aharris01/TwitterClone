from flask import request, jsonify, render_template
from config import app
import re
from markupsafe import escape


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Handle empty values
        if not username or not password:
            return render_template("login.html")

        # Username too large for system
        if len(username) > 80:
            return render_template("login.html")

        # Check if the username is valid
        if not validateUsername(username):
            print("login failed")
            return render_template("login.html")

        return "<p>Good Job!</p>"

    return render_template("login.html")


def validateUsername(username):
    regex = "^[A-Za-z0-9_-]{1,32}$"
    return not (re.search(regex, username) == None)


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)
