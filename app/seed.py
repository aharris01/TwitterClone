import datetime
from config import db, app
from models import User, Post


def seed_data():
    all_users = {u.userName: u for u in User.query.all()}

    posts = [
        Post(
            content="Hello, world! This is my first post.",
            createdAt=datetime.datetime(2023, 9, 1, 9, 15),
            user_id=all_users["alice"].id,
        ),
        Post(
            content="Another day of coding in Python!",
            createdAt=datetime.datetime(2023, 9, 1, 12, 30),
            user_id=all_users["alice"].id,
        ),
        Post(
            content="Has anyone tried the new JavaScript framework?",
            createdAt=datetime.datetime(2023, 9, 2, 8, 10),
            user_id=all_users["bob"].id,
        ),
        Post(
            content="Weekend is here. Time to relax!",
            createdAt=datetime.datetime(2023, 9, 2, 18, 25),
            user_id=all_users["bob"].id,
        ),
        Post(
            content="Using Flask for a new project. Loving its simplicity.",
            createdAt=datetime.datetime(2023, 9, 3, 10, 0),
            user_id=all_users["ch"].id,
        ),
        Post(
            content="Hello from the security team. Remember to use strong pass",
            createdAt=datetime.datetime(2023, 9, 4, 9, 0),
            user_id=all_users["diana"].id,
        ),
        Post(
            content="Trying out some pentesting tools this weekend.",
            createdAt=datetime.datetime(2023, 9, 4, 22, 15),
            user_id=all_users["diana"].id,
        ),
        Post(
            content="Here’s a tip: use venv for Python dependency isolation.",
            createdAt=datetime.datetime(2023, 9, 5, 14, 0),
            user_id=all_users["eve"].id,
        ),
        Post(
            content="Finally finishing up that tutorial on SQLAlchemy seeds.",
            createdAt=datetime.datetime(2023, 9, 6, 8, 45),
            user_id=all_users["frank"].id,
        ),
        Post(
            content="I love a good cup of coffee while I code.",
            createdAt=datetime.datetime(2023, 9, 6, 9, 10),
            user_id=all_users["grace"].id,
        ),
        Post(
            content="Anyone know a good library for data visualization?",
            createdAt=datetime.datetime(2023, 9, 6, 12, 30),
            user_id=all_users["grace"].id,
        ),
        Post(
            content="Morning run done, now onto some front-end bug fixes.",
            createdAt=datetime.datetime(2023, 9, 7, 7, 20),
            user_id=all_users["heidi"].id,
        ),
        Post(
            content="Deployed a new feature yesterday. So far, no issues!",
            createdAt=datetime.datetime(2023, 9, 7, 21, 0),
            user_id=all_users["heidi"].id,
        ),
        Post(
            content="Reading about microservices architecture. Interesting.",
            createdAt=datetime.datetime(2023, 9, 8, 11, 10),
            user_id=all_users["ivan"].id,
        ),
        Post(
            content="Hoping to attend a cybersecurity webinar tomorrow.",
            createdAt=datetime.datetime(2023, 9, 8, 17, 0),
            user_id=all_users["ivan"].id,
        ),
        Post(
            content="Refactoring old code can be strangely satisfying.",
            createdAt=datetime.datetime(2023, 9, 9, 13, 50),
            user_id=all_users["judy"].id,
        ),
        Post(
            content="Just learned about CSP. Great way to prevent XSS!",
            createdAt=datetime.datetime(2023, 9, 9, 15, 20),
            user_id=all_users["judy"].id,
        ),
        Post(
            content="One more post from Bob. Checking out user feed.",
            createdAt=datetime.datetime(2023, 9, 10, 9, 0),
            user_id=all_users["bob"].id,
        ),
        Post(
            content="Database migrations can be scary but are so useful.",
            createdAt=datetime.datetime(2023, 9, 10, 9, 5),
            user_id=all_users["ch"].id,
        ),
        Post(
            content="Finally got test coverage above 90%. Feels good!",
            createdAt=datetime.datetime(2023, 9, 11, 10, 45),
            user_id=all_users["ch"].id,
        ),
        Post(
            content="I prefer dark themes for my IDE.",
            createdAt=datetime.datetime(2023, 9, 11, 13, 0),
            user_id=all_users["eve"].id,
        ),
        Post(
            content="Has anyone used Docker for local dev? It's so convenient.",
            createdAt=datetime.datetime(2023, 9, 12, 10, 0),
            user_id=all_users["frank"].id,
        ),
        Post(
            content="Setting up a CI pipeline to run all tests on commits.",
            createdAt=datetime.datetime(2023, 9, 12, 18, 30),
            user_id=all_users["frank"].id,
        ),
        Post(
            content="Front-end frameworks: React vs. Vue vs. Angular?",
            createdAt=datetime.datetime(2023, 9, 13, 8, 10),
            user_id=all_users["grace"].id,
        ),
        Post(
            content="SQL injection is something to watch out for in forms!",
            createdAt=datetime.datetime(2023, 9, 13, 9, 20),
            user_id=all_users["alice"].id,
        ),
        Post(
            content="Morning debug session. Found a sneaky off-by-one error.",
            createdAt=datetime.datetime(2023, 9, 13, 9, 25),
            user_id=all_users["ivan"].id,
        ),
        Post(
            content="Time for some code review. Collaboration is key.",
            createdAt=datetime.datetime(2023, 9, 14, 14, 5),
            user_id=all_users["heidi"].id,
        ),
        Post(
            content="Reading up on advanced Flask patterns, interesting stuff.",
            createdAt=datetime.datetime(2023, 9, 15, 11, 45),
            user_id=all_users["heidi"].id,
        ),
        Post(
            content="Python 3.12 new features are coming soon.",
            createdAt=datetime.datetime(2023, 9, 15, 12, 0),
            user_id=all_users["eve"].id,
        ),
        Post(
            content="Double-check your session handling for security!",
            createdAt=datetime.datetime(2023, 9, 16, 7, 30),
            user_id=all_users["diana"].id,
        ),
    ]
    print("here")
    db.session.bulk_save_objects(posts)
    db.session.commit()
    print("Seed data inserted successfully!")


with app.app_context():
    seed_data()
