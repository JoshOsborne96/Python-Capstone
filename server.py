from flask import (Flask, render_template, redirect, url_for, request, session, flash)
from model import connect_to_db, Goal, db
from forms import GoalForm
import crud, logging

from jinja2 import StrictUndefined

app = Flask(__name__)
connect_to_db(app)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.errorhandler(404)
def error_404(e):

    return render_template("404.html", page ="404")


@app.route("/")
def home():
    """View homepage."""

    goal_form = GoalForm()

    return render_template("home.html", goal_form=goal_form, page = "home")

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
        session["user_id"] = user.id
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/logout")
def logout():
   """Log user out."""

   if 'user_email' not in session:
        flash("Please log in or create an account")
        return redirect("/")
        
   else:
        del session["user_email"]
        del session["user_id"]
        flash("Logged out.")

   return redirect("/")

@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    """Create a new user"""

    logging.error('This is an error message')

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/pending-goals")
def pending_goals():
    """View a user's pending goals"""
    if 'user_email' not in session:
        flash("Please log in or create an account")
        
        return redirect("/")
    else:
        goals = crud.get_pending_goals(session["user_id"])

    return render_template("pending_goals.html", goals=goals, page = "pending-goals")

@app.route("/complete-goals")
def complete_goals():
    """View a user's completed goals"""


    if "user_email" not in session:
        flash("Please log in or create an account")
        return redirect("/")
    else:
        goals= crud.get_complete_goals(session["user_id"])
        return render_template("complete_goals.html", goals=goals, page = "complete-goals")

@app.route("/add-goal", methods=["GET", "POST"])
def add_goal():
    

    if "user_email" not in session:
            flash("Please log in or create an account")
            return redirect("/")
    else:
            goal_form = GoalForm()
            if request.method == "POST":
                if goal_form.validate_on_submit():
                    description = goal_form.description.data
                    picture_path = goal_form.picture_path.data
                    deadline = goal_form.deadline.data
                    complete = False
                    user_id = session["user_id"]

                    new_goal = Goal(description, picture_path, deadline, complete, user_id)
                    db.session.add(new_goal)
                    db.session.commit()

                    return redirect(url_for("pending_goals"))
                else: 
                    return redirect(url_for("home"))
            else:
                return render_template("add_goal.html", goal_form= goal_form, page = "add-goal")

@app.route("/update-goal/<goal_id>", methods=["GET", "POST"])
def update_goal(goal_id):
    form = GoalForm()
    goal = Goal.query.get(goal_id)
    if request.method == "POST":
        if form.validate_on_submit():
            goal.description = form.description.data
            goal.picture_path = form.picture_path.data
            goal.deadline = form.deadline.data
            goal.complete = form.complete.data

            db.session.add(goal)
            db.session.commit()
            return redirect(url_for("pending_goals"))
        else:
            return redirect(url_for("home"))

    else:
        return render_template("update_goal.html", goal=goal, form=form, page = "home")

@app.route("/delete-goal/<goal_id>")
def delete_goal(goal_id):

    goal = Goal.query.get(goal_id)
    goals = crud.get_pending_goals(session["user_id"])

    db.session.delete(goal)
    db.session.commit()
    flash("Goal deleted!")

    return render_template("pending_goals.html", goal=goal, goals=goals, page="pending-goals")

# def app(env, res):
#     connect_to_db(app)
#     app.run(host="0.0.0.0", port=8080, debug=True)

# if __name__ == "__main__":
#     connect_to_db(app)
#     app.run(host="0.0.0.0", port=8080, debug=True)