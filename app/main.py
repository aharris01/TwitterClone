from flask import request, jsonify
from models import User
from config import app, db


@app.route("/createuser/<username>")
def createUser(username):
    new_user = User(userName=username)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return e

    return f"<p>User: {username} created</p>"


@app.route("/listusers")
def listUsers():
    users = User.query.all()
    userString = ""
    for user in users:
        userString += user.__str__()
    return f"List of users:{userString}"


@app.route("/listuser/<int:userID>")
def listUser(userID):
    user = db.session.execute(db.select(User).where(User.id == userID)).scalars()
    print(user)

    return f"<p>User: {user}</p>"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(ssl_context="adhoc", debug=True)
