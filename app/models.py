from config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=False, nullable=False)

    def to_json(self):
        return {"id": self.id, "userName": self.userName}

    def __str__(self):
        return f"ID:{self.id}, userName:{self.userName}\t"
