from flask import request, jsonify
from models import User
from config import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(ssl_context="adhoc", debug=True)
