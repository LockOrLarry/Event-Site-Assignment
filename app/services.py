from . import db
from .models import User, Event, Booking


def get_user_by_id(user_id):
    return db.session.get(User, user_id)


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


def create_booking(user_id, event_id, quantity):
    user = get_user_by_id(user_id)

    if user is None:
        return None, 'User not found'

    event = get_event_by_id(event_id)

    if event is None:
        return None, 'Event not found'

    if quantity < 1:
        return None, 'Booking quantity must be at least 1'

    if event.status != 'Open':
        return None, 'This event is not available for booking'

    tickets_remaining = get_tickets_remaining(event)

    if quantity > tickets_remaining:
        return None, f'Only {tickets_remaining} tickets are available'

    booking = Booking(
        user_id=user_id,
        event_id=event.id,
        quantity=quantity,
        price=event.price
    )

    db.session.add(booking)

    if quantity == tickets_remaining:
        event.status = 'Sold Out'

    db.session.commit()

    return booking, None
    

    