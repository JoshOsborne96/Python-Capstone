"""CRUD operations."""

from model import db, User, Goal, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(
        email=email,
        password=password,
        )

    return user

def create_goal(description, picture_path, deadline, complete, user_id):
    """Create and return a new goal."""

    goal = Goal(
        description=description,
        picture_path=picture_path,
        deadline=deadline,
        complete=complete,
        user_id=user_id
        )

    return goal

def get_pending_goals(user_id):
    """Return all non-complete goals for a user"""

    return Goal.query.filter(Goal.user_id == user_id, Goal.complete == False).all()

def get_complete_goals(user_id):

    """Return all completed goals for a user"""

    return Goal.query.filter(Goal.user_id == user_id, Goal.complete == True).all()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_id(email):
    """Get a user id by email"""

    return User.query.filter(User.id == id).first()





if __name__ == '__main__':
    from server import app
    connect_to_db(app)

# user1 = create_user("tester1", "testpass", "fn-test", "ln-test" )

# goal1 = create_goal("get this app done", "test url", "2/1/2023")