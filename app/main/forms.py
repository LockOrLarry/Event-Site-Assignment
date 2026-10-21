from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField, SubmitField, IntegerField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, ValidationError
from wtforms.fields import DateField, TimeField, DecimalField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from datetime import datetime



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

class EventCreationForm(FlaskForm):
    title = StringField(
        'Event name',
        validators=[InputRequired(), Length(max=150)]
    )

    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[InputRequired()]
    )

    description = TextAreaField(
        'Description',
        validators=[InputRequired()]
    )

    event_date = DateField(
        'Event date',
        validators=[InputRequired()]
    )

    start_time = TimeField(
        'Start time',
        validators=[InputRequired()]
    )

    end_time = TimeField(
        'End time',
        validators=[InputRequired()]
    )

    venue_name = StringField(
        'Venue name',
        validators=[InputRequired(), Length(max=100)]
    )

    address = StringField(
        'Address',
        validators=[InputRequired(), Length(max=150)]
    )

    suburb = StringField(
        'Suburb',
        validators=[InputRequired(), Length(max=100)]
    )

    state = SelectField(
        'State',
        choices=[
            ('QLD', 'QLD'),
            ('NSW', 'NSW'),
            ('VIC', 'VIC'),
            ('SA', 'SA'),
            ('WA', 'WA'),
            ('TAS', 'TAS'),
            ('ACT', 'ACT'),
            ('NT', 'NT')
        ],
        validators=[InputRequired()]
    )

    postcode = StringField(
        'Postcode',
        validators=[
            InputRequired(),
            Length(min=4, max=4)
        ]
    )

    price = DecimalField(
        'Ticket price',
        places=2,
        validators=[InputRequired(), NumberRange(min=0.01)]
    )

    capacity = IntegerField(
        'Ticket capacity',
        validators=[InputRequired(), NumberRange(min=1)]
    )

    image = FileField(
        'Event image',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only.')
        ]
    )

    age_suitability = SelectField(
        'Age suitability',
        choices=[
            ('All Ages', 'All Ages'),
            ('13+', '13+'),
            ('16+', '16+'),
            ('18+', '18+')
        ],
        validators=[InputRequired()]
    )

    dietary_options = SelectField(
        'Dietary options',
        choices=[
            ('Multiple dietary options', 'Multiple dietary options'),
            ('Vegetarian', 'Vegetarian'),
            ('Vegan', 'Vegan'),
            ('Gluten-Free', 'Gluten-Free'),
            ('No specific options', 'No specific options')
        ],
        validators=[InputRequired()]
    )

    additional_details = TextAreaField(
        'Additional details'
    )

    acknowledgement_type = SelectField(
        'Acknowledgement of Country',
        choices=[
            ('None', 'None'),
            ('Generic', 'Generic acknowledgement'),
            ('Enhanced', 'Custom acknowledgement')
        ],
        default='None',
        validators=[InputRequired()]
    )

    acknowledgement_text = TextAreaField(
        'Custom acknowledgement',
        validators=[Length(max=2000)]
    )

    def validate_end_time(self, field):
        if self.start_time.data and field.data:
            if field.data <= self.start_time.data:
                raise ValidationError(
                    'End time must be later than start time.'
                )

    def validate_event_date(self, field):
        if field.data is None or self.start_time.data is None:
            return

        event_start = datetime.combine(
            field.data,
            self.start_time.data
        )

        if event_start <= datetime.now():
            raise ValidationError(
                'The event start date and time must be in the future.'
            )

    def validate_acknowledgement_text(self, field):
        if self.acknowledgement_type.data == 'Enhanced':
            if not field.data or not field.data.strip():
                raise ValidationError(
                    'Please provide your custom Acknowledgement of Country.'
                )

    submit = SubmitField('Create Event')

class EventEditForm(EventCreationForm):
    image = FileField(
        'Event image',
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'webp'],
                'Images only.'
            )
        ]
    )

    submit = SubmitField('Save Changes')