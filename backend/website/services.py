from . import db
from .models import Event

def get_all_events():
    return db.session.scalars(
        db.select(Event)
    ).all()


def get_event_by_id(event_id):
    return db.session.get(Event, event_id)


def get_tickets_sold(event):
    return sum(
        booking.quantity
        for booking in event.bookings
    )


def get_tickets_remaining(event):
    return event.capacity - get_tickets_sold(event)


def get_events_by_category(category_id):
    return db.session.scalars(
        db.select(Event).where(Event.category_id == category_id)
    ).all()


def get_events_by_status(status):
    return db.session.scalars(
        db.select(Event).where(Event.status == status)
    ).all()