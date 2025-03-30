from flask import request, jsonify, render_template, redirect, url_for, flash, session
from config import app, db
from models import User
from argon2 import PasswordHasher
import re
import os

app.config["SECRET_KEY"] = os.urandom(24)


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

        # Check if the username is valid
        if not validateUsername(username):
            flash("Invalid username", "error")
            return render_template("login.html")

        user = db.session.query(User).filter_by(userName=username).first()

        if user and user.checkPassword(password):
            session["user_id"] = user.id
            session["username"] = user.userName
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("That user does not exist", "error")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"Username: {username}, Password: {password}")

        # Handle empty values
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("createuser.html")

        # Check if username is valid
        if not validateUsername(username):
            flash(
                "Invalid username. Must contain only letters, numbers, underscores or hyphens and be at most 32 characters long",
                "error",
            )
            return render_template("createuser.html")

        newUser = User(userName=username)
        newUser.setPassword(password)

        try:
            db.session.add(newUser)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("An error occurred creating the account", "error")

    return render_template("createuser.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    return


@app.route("/changepassword", methods=["PATCH", "GET"])
def changePassword():
    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))
    elif request.method == "PATCH":
        print(
            f"Current password: {request.form.get('current_password')}, New Password: {request.form.get('new_password')}"
        )
        newPassword = request.form.get("password")
        userID = session["user_id"]

        user = db.session.query(User).where(id=userID)
        user.setPassword(newPassword)
        db.session.commit()

    return render_template("changepassword.html")


def validateUsername(username):
    regex = "^[A-Za-z0-9_-]{1,32}$"
    return not (re.search(regex, username) == None)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(ssl_context="adhoc", debug=True)
