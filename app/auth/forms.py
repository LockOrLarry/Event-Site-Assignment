from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Regexp, Email, EqualTo, Length


 # this is the registration form
class RegisterForm(FlaskForm):
    first_name=StringField("First Name", validators=[InputRequired(), Regexp("^[a-zA-Z]+$"), Length(min=1, max=25)])
    surname=StringField("Last Name", validators=[InputRequired(), Regexp("^[a-zA-Z]+$"), Length(min=1, max=25)])
    email = StringField("Email Address", validators=[InputRequired(), Length(min=6, max=35), Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    phone=StringField("Phone", validators=[InputRequired(), Regexp("^[0-9]*$")])
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