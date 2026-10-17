import json
from . import db, encoder
from datetime import datetime
from .models import User, Event, Booking, Category, Comment


def get_user_by_id(user_id):
    return db.session.get(User, user_id)


def get_all_events():
    return db.session.scalars(
        db.select(Event)
    ).all()


def get_all_categories():
    return db.session.scalars(
        db.select(Category).order_by(Category.id)
    ).all()


def get_featured_events(limit=4):
    now = datetime.now()

    return db.session.scalars(
        db.select(Event)
        .where(
            Event.status == 'Open',
            Event.event_date > now
        )
        .order_by(Event.event_date)
        .limit(limit)
    ).all()


def get_event_by_id(event_id):
    return db.session.get(Event, event_id)


def get_effective_event_status(event):
    event_end = datetime.combine(
        event.event_date.date(),
        event.end_time
    )

    if event_end <= datetime.now():
        return 'Completed'

    return event.status


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


def create_comment(user_id, event_id, text):
    event = get_event_by_id(event_id)

    text = text.strip()

    if not text:
        return None, 'Comment cannot be empty'

    comment = Comment(
        user_id=user_id,
        event_id=event.id,
        text=text
    )

    db.session.add(comment)
    db.session.commit()

    return comment, None


def create_booking(user_id, event_id, quantity):
    user = get_user_by_id(user_id)

    if user is None:
        return None, 'User not found'

    event = get_event_by_id(event_id)

    if event is None:
        return None, 'Event not found'

    if quantity < 1:
        return None, 'Booking quantity must be at least 1'

    if get_effective_event_status(event) != 'Open':
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
    

def get_bookings_by_user(user_id):
    return db.session.scalars(
        db.select(Booking)
        .where(Booking.user_id == user_id)
        .order_by(Booking.booking_date.desc())
    ).all()

def create_event(
    creator_id,
    form,
    image_path
):
    event_datetime = datetime.combine(
        form.event_date.data,
        form.start_time.data
    )

    location = (
        f"{form.address.data}, "
        f"{form.suburb.data}, "
        f"{form.state.data} "
        f"{form.postcode.data}"
    )

    acknowledgement_type = form.acknowledgement_type.data

    if acknowledgement_type == 'Generic':
        acknowledgement_text = (
            'We acknowledge the Traditional Custodians of the land '
            'on which this event takes place and pay our respects '
            'to Elders past and present.'
        )
    elif acknowledgement_type == 'Enhanced':
        acknowledgement_text = form.acknowledgement_text.data.strip()
    else:
        acknowledgement_text = None

    event = Event(
        creator_id=creator_id,
        category_id=form.category_id.data,
        title=form.title.data.strip(),
        description=form.description.data.strip(),
        event_date=event_datetime,
        end_time=form.end_time.data,
        location=location,
        venue_name=form.venue_name.data.strip(),
        address=form.address.data.strip(),
        suburb=form.suburb.data.strip(),
        state=form.state.data,
        postcode=form.postcode.data.strip(),
        price=form.price.data,
        capacity=form.capacity.data,
        image_path=image_path,
        age_suitability=form.age_suitability.data,
        dietary_options=form.dietary_options.data,
        additional_details=form.additional_details.data,
        status='Open',
        acknowledgement_type=acknowledgement_type,
        acknowledgement_text=acknowledgement_text
    )

    db.session.add(event)
    db.session.flush()
    update_event_embedding(event)
    db.session.commit()

    return event


def build_embedding_text(event):
    return f"{event.title}. {event.category.name}. {event.description}"


def update_event_embedding(event):
    embedding = encoder.encode(build_embedding_text(event))
    event.description_embedding = json.dumps(embedding.tolist())