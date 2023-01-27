from flask import (Flask, render_template, redirect, url_for, request)
from flask_user import login_required
from model import connect_to_db, Goal, db
from forms import GoalForm
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    goal_form = GoalForm()
    goals = crud.get_pending_goals(2)

    return render_template("home.html", goals=goals, goal_form=goal_form)

@app.route("/complete-goals")
def complete_goals():
    """View user's completed goals"""

    goals= crud.get_complete_goals(2)

    return render_template("complete_goals.html", goals=goals)

@app.route("/login")
def login():
    """View login/create user page."""


    return render_template("login.html")

@app.route("/add-goal", methods=["GET", "POST"])
def add_goal():
    goal_form = GoalForm()

    if goal_form.validate_on_submit():
        description = goal_form.description.data
        picture_path = goal_form.picture_path.data
        deadline = goal_form.deadline.data
        complete = False
        user_id = goal_form.user_id.data

        new_goal = Goal(description, picture_path, deadline, complete, user_id)
        db.session.add(new_goal)
        db.session.commit()

        return "Successfuly added goal"
    else: 
        return redirect(url_for("homepage"))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", port=5000, debug=True)