from flask import request, jsonify, render_template, redirect, url_for, flash
from config import app, db
import re
from markupsafe import escape


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Handle empty values
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("login.html")

        # Username too large for system
        if len(username) > 80:
            flash("Username too large", "error")
            return render_template("login.html")

        # Check if the username is valid
        if not validateUsername(username):
            return render_template("login.html")

        return "<p>Good Job!</p>"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


def validateUsername(username):
    regex = "^[A-Za-z0-9_-]{1,32}$"
    return not (re.search(regex, username) == None)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(ssl_context="adhoc", debug=True)
