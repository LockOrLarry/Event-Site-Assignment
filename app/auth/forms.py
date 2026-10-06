from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


 # this is the registration form
class RegisterForm(FlaskForm):
    first_name=StringField("First Name", validators=[InputRequired()])
    surname=StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    phone=StringField("Phone", validators=[InputRequired()])
    address=StringField("Address", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired(),
                      EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])

    # submit button
    submit = SubmitField("Register")

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired('Enter email'), Email("Please enter a valid email")])
    password=PasswordField("Password", validators=[InputRequired('Enter password')])
    submit = SubmitField("Login")