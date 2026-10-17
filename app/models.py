from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(254),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    events = db.relationship(
        'Event',
        back_populates='creator'
    )

    bookings = db.relationship(
        'Booking',
        back_populates='user'
    )

    comments = db.relationship(
        'Comment',
        back_populates='user'
    )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    description = db.Column(db.Text, nullable=True)

    events = db.relationship(
        'Event',
        back_populates='category'
    )


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_embeddingg = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    venue_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    suburb = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(3), nullable=False)
    postcode = db.Column(db.String(4), nullable=False)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    image_path = db.Column(db.String(255), nullable=False)

    age_suitability = db.Column(
        db.String(20),
        nullable=False,
        default='All Ages'
    )

    dietary_options = db.Column(
        db.String(50),
        nullable=False,
        default='Multiple dietary options'
    )

    additional_details = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default='Open'
    )

    acknowledgement_type = db.Column(
        db.String(20),
        nullable=False,
        default='None'
    )

    acknowledgement_text = db.Column(db.Text, nullable=True)

    creator = db.relationship(
        'User',
        back_populates='events'
    )

    category = db.relationship(
        'Category',
        back_populates='events'
    )

    bookings = db.relationship(
        'Booking',
        back_populates='event'
    )

    comments = db.relationship(
        'Comment',
        back_populates='event'
    )

    __table_args__ = (
        db.CheckConstraint(
            'price > 0',
            name='check_event_price_positive'
        ),
        db.CheckConstraint(
            'capacity > 0',
            name='check_event_capacity_positive'
        ),
        db.CheckConstraint(
            "status IN ('Open', 'Inactive', 'Sold Out', 'Cancelled')",
            name='check_event_status_valid'
        ),
        db.CheckConstraint(
            "acknowledgement_type IN ('None', 'Generic', 'Enhanced')",
            name='check_acknowledgement_type_valid'
        ),
    )


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship(
        'User',
        back_populates='bookings'
    )

    event = db.relationship(
        'Event',
        back_populates='bookings'
    )

    __table_args__ = (
        db.CheckConstraint(
            'quantity >= 1',
            name='check_booking_quantity_positive'
        ),
        db.CheckConstraint(
            'price > 0',
            name='check_booking_price_positive'
        )
    )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        nullable=False
    )

    text = db.Column(db.Text, nullable=False)

    comment_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship(
        'User',
        back_populates='comments'
    )

    event = db.relationship(
        'Event',
        back_populates='comments'
    )
