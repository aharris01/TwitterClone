from config import db
from argon2 import PasswordHasher
from datetime import datetime


# The User class stores passwords with Argon2id hashing
# The parameters were chosen based on https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#password-hashing-algorithms
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(32), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)

    def setPassword(self, password):
        ph = PasswordHasher(time_cost=5, memory_cost=12288, parallelism=1)
        self.passwordHash = ph.hash(password)

    def checkPassword(self, password):
        ph = PasswordHasher(time_cost=5, memory_cost=12288, parallelism=1)
        try:
            return ph.verify(self.passwordHash, password)
        except Exception as e:
            return False

    def to_json(self):
        return {"id": self.id, "userName": self.userName}


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime, default=datetime.today())

    user = db.relationship("User", backref=db.backref("posts", lazy="dynamic"))

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "createdAt": self.createdAt,
            "userID": self.user_id,
        }
