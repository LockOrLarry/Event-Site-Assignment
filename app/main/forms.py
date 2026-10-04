from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField, SubmitField, IntegerField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange


class BookingForm(FlaskForm):
    quantity = IntegerField(
        'Number of tickets',
        default=1,
        validators=[InputRequired(), NumberRange(min=1)]
    )
    submit = SubmitField('Book Tickets')
