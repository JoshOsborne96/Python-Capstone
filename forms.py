from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Length

class GoalForm(FlaskForm):
    description = TextAreaField('Goal description')
    picture_path = StringField('Image URL')
    deadline = DateField("Deadline")
    complete = BooleanField("Completed?")
    submit = SubmitField("Submit")

    def update_goal(self, goals):
        self.goal
    
