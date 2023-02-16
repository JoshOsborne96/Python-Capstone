import os, logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable = False)
    

    goals = db.relationship("Goal", backref = "user", lazy = True)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        
        

    def __repr__(self):
        return f"<User user_id={self.id} email={self.email}>"
    
class Goal(db.Model):
    """A goal."""

    __tablename__ = "goals"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.Text)
    picture_path = db.Column(db.String)
    deadline = db.Column(db.Date)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, description, picture_path, deadline, complete, user_id):
        self.description = description
        self.picture_path = picture_path
        self.deadline = deadline
        self.complete = complete
        self.user_id =user_id

    def __repr__(self):
        return f"<Goal goal_id={self.id} description={self.description}>"


def connect_to_db(flask_app, echo=True):
    logging.error('This is an error message in model.py')
    fly_db_url = os.environ["DATABASE_URL"]
    correct_db_url = fly_db_url.replace("postgres", "postgresql", 1)
    print(correct_db_url)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = correct_db_url
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")
    db.create_all()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)