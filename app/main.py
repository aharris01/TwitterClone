from flask import (
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    Response,
)
from sqlalchemy.exc import IntegrityError
from config import app, db, bl
from models import User, Post
from datetime import datetime
import bleach
import re
import os

app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_COOKIE_SECURE"] = True


def authenticationCheck():
    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))


# Basic CSP allowing scripts, styles, etc. only from the same origin
@app.after_request
def applyCsp(response: Response) -> Response:
    csp = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "object-src 'none'; "
    )
    response.headers["Content-Security-Policy"] = csp
    return response


# Redirect to login
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

        # Find user (if they exist) in database
        user = db.session.query(User).filter_by(userName=username).first()

        # Check if the password is correct
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

        # Check if password follows the rules or is in bloom filter
        if not validatePassword(password):
            flash("Password too weak", "error")
            return render_template("createuser.html")

        # Create a new user object
        newUser = User(userName=username)

        # Set their password hash
        newUser.setPassword(password)

        # Attempt to add user to database
        try:
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("That username already exists", "error")
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("An error occurred creating the account", "error")

    return render_template("createuser.html")


@app.route("/dashboard")
def dashboard():
    notAuthenticated = authenticationCheck()
    if notAuthenticated:
        return notAuthenticated
    # Preload 10 most recent posts
    posts = db.session.query(Post).order_by(Post.createdAt.desc()).limit(10).all()
    data = []
    for post in posts:
        data.append(
            {
                "id": post.id,
                "content": post.content,
                "createdAt": post.createdAt,
                "author": post.user.userName,
            }
        )

    return render_template("dashboard.html", username=session["username"], posts=data)


@app.route("/api/recentposts")
def recentPosts():
    notAuthenticated = authenticationCheck()
    if notAuthenticated:
        return notAuthenticated

    offset = request.args.get("offset", 0)
    try:
        offset = int(offset)
    except ValueError:
        return jsonify({})

    posts = (
        db.session.query(Post)
        .order_by(Post.createdAt.desc())
        .offset(offset)
        .limit(10)
        .all()
    )

    data = []
    for post in posts:
        data.append(
            {
                "id": post.id,
                "content": post.content,
                "createdAt": post.createdAt.strftime("%Y-%m-%d %H:%M"),
                "author": post.user.userName,
            }
        )

    return jsonify(data)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/changepassword", methods=["POST", "GET"])
def changePassword():
    notAuthenticated = authenticationCheck()
    if notAuthenticated:
        return notAuthenticated
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

        # Change users password
        user.setPassword(newPassword)
        db.session.commit()
        flash("Password updated successfully", "success")
        return redirect(url_for("dashboard"))

    return render_template("changepassword.html")


@app.route("/createpost", methods=["GET", "POST"])
def createPost():
    notAuthenticated = authenticationCheck()
    if notAuthenticated:
        return notAuthenticated
    if request.method == "POST":
        content = request.form.get("content")

        # Check for empty content
        if not content:
            flash("Post content cannot be empty", "error")
            return render_template("createpost.html")

        # Remove any HTML tags entirely
        safeContent = bleach.clean(content, strip=True)

        if safeContent == "" or safeContent == None:
            flash("Error creating post", "error")
            return redirect(url_for("dashboard"))

        # Save safe content in database with associated user and when it was created
        post = Post(
            content=safeContent, user_id=session["user_id"], createdAt=datetime.now()
        )
        db.session.add(post)
        db.session.commit()

        flash("Post successfully created", "success")
        return redirect(url_for("dashboard"))

    return render_template("createpost.html")


# A username can only contain letters, numbers, underscores, and hyphens to help mitigate injection attacks
def validateUsername(username):
    regex = "^[A-Za-z0-9_-]{1,32}$"
    return not (re.search(regex, username) == None)


# A password can be any ASCII printable character, but must be within 8-64 characters
# A bloom filter is used to prevent some commonly used passwords
def validatePassword(password):
    regex = "^[\x20-\x7e]{8,64}$"
    if re.search(regex, password) is None:
        return False

    if bl is not None and bl.check(password):
        return False

    return True


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(ssl_context="adhoc", debug=True)
