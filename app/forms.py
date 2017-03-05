from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    gender = SelectField(label='State', choices=[("Male", "Male"), ("Female", "Female")])
    biography = StringField('Biography', validators=[InputRequired()])