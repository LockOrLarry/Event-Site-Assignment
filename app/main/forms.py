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

class CommentForm(FlaskForm):
    text = TextAreaField(
        'Share your thoughts',
        validators=[
            InputRequired(message='Please write a comment before posting.'),
            Length(max=1000, message='Comment cannot exceed 1000 characters.')
        ]
    )
    submit = SubmitField('Post Comment')
