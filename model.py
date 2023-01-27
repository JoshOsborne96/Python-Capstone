import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    

    goals = db.relationship("Goal", backref = "user", lazy = True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        
        

    def __repr__(self):
        return f"<User user_id={self.id} username={self.username}>"
    
class Goal(db.Model):
    """A goal."""

    __tablename__ = "goals"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.Text)
    picture_path = db.Column(db.String)
    deadline = db.Column(db.Date)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, description, picture_path, deadline, complete, user_id):
        self.description = description
        self.picture_path = picture_path
        self.deadline = deadline
        self.complete = complete
        self.user_id =user_id

    def __repr__(self):
        return f"<Goal goal_id={self.id} description={self.description}>"


def connect_to_db(flask_app, db_uri="postgresql://postgres:Blakely26!@localhost:5432/python-capstone-db", echo=True):
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)