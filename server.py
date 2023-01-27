from flask import (Flask, render_template, redirect, url_for, request, session, flash)
from flask_user import login_required
from model import connect_to_db, Goal, db
from forms import GoalForm
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

user_id = 1

@app.route("/")
def home():
    """View homepage."""

    goal_form = GoalForm()

    return render_template("home.html", goal_form=goal_form)

@app.route("/pending-goals")
def pending_goals():
    """View a user's pending goals"""

    goals = crud.get_pending_goals(1)

    return render_template("pending_goals.html", goals=goals)

@app.route("/complete-goals")
def complete_goals():
    """View a user's completed goals"""

    goals= crud.get_complete_goals(2)

    return render_template("complete_goals.html", goals=goals)

@app.route("/login", methods=["GET", "POST"])
def login():
    """View login/create user page."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/add-goal", methods=["GET", "POST"])
def add_goal():
    goal_form = GoalForm()

    if request.method == "POST":
        if goal_form.validate_on_submit():
            description = goal_form.description.data
            picture_path = goal_form.picture_path.data
            deadline = goal_form.deadline.data
            complete = False
            user_id = goal_form.user_id.data

            new_goal = Goal(description, picture_path, deadline, complete, user_id)
            db.session.add(new_goal)
            db.session.commit()

            return redirect(url_for("pending_goals"))
        else: 
            return redirect(url_for("home"))
    else:
        return render_template("add_goal.html", goal_form= goal_form)
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", port=5000, debug=True)