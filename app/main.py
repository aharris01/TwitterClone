from flask import request, jsonify, render_template, redirect, url_for, flash, session
from config import app, db, bl
from models import User
import re
import os

app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_COOKIE_SECURE"] = True
# app.config["SESSION_COOKIE_SAMESITE"] = True


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
            flash("Invalild Username or Password", "error")
            return render_template("login.html")

        # Check if the username is valid
        if not validateUsername(username):
            flash("Invalid Username or Password", "error")
            return render_template("login.html")

        user = db.session.query(User).filter_by(userName=username).first()

        if user and user.checkPassword(password):
            session["user_id"] = user.id
            session["username"] = user.userName
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Username or Password", "error")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

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

        if not validatePassword(password):
            flash("Password too weak", "error")
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
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/changepassword", methods=["POST", "GET"])
def changePassword():
    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))
    if request.method == "POST":
        currentPassword = request.form.get("current_password")
        newPassword = request.form.get("new_password")
        confirmPassword = request.form.get("confirm_password")

        # Handle empty values
        if not currentPassword or not newPassword or not confirmPassword:
            flash("All fields are required", "error")
            return render_template("changepassword.html")

        # New passwords match
        if newPassword != confirmPassword:
            flash("New passwords do not match", "error")
            return render_template("changepassword.html")

        # Check password strength (will be updated later)
        if not validatePassword(newPassword):
            flash(
                "Password is too weak. Password can't be easily guessable and must be at least 8 characters long, and contain only printable characters",
                "error",
            )
            return render_template("changepassword.html")

        # Get user from database
        user = db.session.query(User).where(User.id == session["user_id"]).first()

        # Confirm authentication
        if not user.checkPassword(currentPassword):
            flash("Current password is incorrect", "error")
            return render_template("changepassword.html")

        user.setPassword(newPassword)
        db.session.commit()
        flash("Password updated successfully", "success")
        return render_template("dashboard.html")

    return render_template("changepassword.html")


def validateUsername(username):
    regex = "^[A-Za-z0-9_-]{1,32}$"
    return not (re.search(regex, username) == None)


def validatePassword(password):
    regex = "^[\x20-\x7e]{8,64}$"
    if re.search(regex, password) is None:
        return False

    print(bl.check(password))
    if bl is not None and bl.check(password):
        print(f"bl: {bl}, validity: {bl.check(password)}")
        return False

    return True


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(ssl_context="adhoc", debug=True)
