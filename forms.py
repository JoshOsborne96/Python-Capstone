from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Length

class GoalForm(FlaskForm):
    description = TextAreaField('Goal description')
    picture_path = StringField('Image URL')
    deadline = DateField("Deadline")
    complete = False
    user_id = IntegerField("User ID #")
    submit = SubmitField("submit")

    def update_goal(self, goals):
        self.goal