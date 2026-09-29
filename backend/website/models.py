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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    description = db.Column(db.Text, nullable=True)


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
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    image_path = db.Column(db.String(255), nullable=False)

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