from config import db
from argon2 import PasswordHasher


# The User class stores passwords with Argon2id hashing
# The parameters were chosen based on https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#password-hashing-algorithms
class User(db.Model):
    id = db.Column(db.Integer, primaryKey=True)
    userName = db.Column(db.String(32), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)

    def setPassword(self, password):
        ph = PasswordHasher(time_cost=5, memory_cost=12288, parallelism=1)
        self.passwordHash = ph.hash(password)

    def checkPassword(self, password):
        ph = PasswordHasher(time_cost=5, memory_cost=12288, parallelism=1)
        return ph.verify(self.passwordHash, password)

    def to_json(self):
        return {"id": self.id, "userName": self.userName}
