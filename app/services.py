import json, re
from . import db, encoder
from sentence_transformers import util
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


def update_event(event, form, image_path=None):
    tickets_sold = get_tickets_sold(event)

    if form.capacity.data < tickets_sold:
        return (
            f'Capacity cannot be lower than the '
            f'{tickets_sold} tickets already booked.'
        )

    event.category_id = form.category_id.data
    event.title = form.title.data.strip()
    event.description = form.description.data.strip()

    event.event_date = datetime.combine(
        form.event_date.data,
        form.start_time.data
    )
    event.end_time = form.end_time.data

    event.venue_name = form.venue_name.data.strip()
    event.address = form.address.data.strip()
    event.suburb = form.suburb.data.strip()
    event.state = form.state.data
    event.postcode = form.postcode.data.strip()

    event.location = (
        f"{event.address}, {event.suburb}, "
        f"{event.state} {event.postcode}"
    )

    event.price = form.price.data
    event.capacity = form.capacity.data

    event.age_suitability = form.age_suitability.data
    event.dietary_options = form.dietary_options.data
    event.additional_details = form.additional_details.data

    event.acknowledgement_type = form.acknowledgement_type.data

    if event.acknowledgement_type == 'Generic':
        event.acknowledgement_text = (
            'We acknowledge the Traditional Custodians of the land '
            'on which this event takes place and pay our respects '
            'to Elders past and present.'
        )
    elif event.acknowledgement_type == 'Enhanced':
        event.acknowledgement_text = (
            form.acknowledgement_text.data.strip()
        )
    else:
        event.acknowledgement_text = None

    if image_path is not None:
        event.image_path = image_path

    if event.status != 'Cancelled':
        if tickets_sold >= event.capacity:
            event.status = 'Sold Out'
        else:
            event.status = 'Open'

    update_event_embedding(event)

    db.session.commit()

    return None


def build_embedding_text(event):
    return f"{event.title}. {event.category.name}. {event.description}"


def update_event_embedding(event):
    embedding = encoder.encode(build_embedding_text(event))
    event.description_embedding = json.dumps(embedding.tolist())


SEARCH_MIN_SCORE = 0.2
SEARCH_RELATIVE_SCORE = 0.75
KEYWORD_WEIGHT = 0.5

STOP_WORDS = {'a', 'an', 'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on', 'at', 'with', 'is', 'I', 'can', 'where', 'what', 'how', 'food', 'event'}


def get_search_terms(query):
    words = re.findall(r"[a-z0-9']+", query.lower())
    return [word for word in words if word not in STOP_WORDS and len(word) > 1]


def contains_word(text, word):
    return re.search(r'\b' + re.escape(word), text.lower()) is not None


def get_keyword_score(query, event):
    terms = get_search_terms(query)

    if not terms:
        return 0.0

    if query.lower().strip() in event.title.lower():
        return 1.0

    score = 0.0

    for term in terms:
        if contains_word(event.title, term):
            score += 1.0
        elif contains_word(event.category.name, term):
            score += 0.6
        elif contains_word(event.description, term):
            score += 0.4

    return score / len(terms)


def has_title_or_category_match(query, event):
    return any(
        contains_word(event.title, term) or contains_word(event.category.name, term)
        for term in get_search_terms(query)
    )


def search_events(query, limit=8):
    query_embedding = encoder.encode(query)

    events = db.session.scalars(
        db.select(Event).where(Event.description_embedding.is_not(None))
    ).all()

    if not events:
        return []

    scored = []

    for event in events:
        event_embedding = json.loads(event.description_embedding)
        ai_score = util.cos_sim(query_embedding, event_embedding).item()
        keyword_score = get_keyword_score(query, event)
        scored.append((ai_score, keyword_score, event))

    best_ai_score = max(ai_score for ai_score, keyword_score, event in scored)
    ai_cutoff = best_ai_score * SEARCH_RELATIVE_SCORE

    results = []

    for ai_score, keyword_score, event in scored:
        relevant_events = best_ai_score >= SEARCH_MIN_SCORE and ai_score >= ai_cutoff

        if relevant_events or has_title_or_category_match(query, event):
            results.append((ai_score + KEYWORD_WEIGHT * keyword_score, event))

    results.sort(key=lambda result: result[0], reverse=True)

    return [event for score, event in results[:limit]]

def keyword_search_events(query, limit=8):
    terms = get_search_terms(query)

    if not terms:
        return []

    statement = db.select(Event).join(Event.category)

    for term in terms:
        pattern = f"%{term}%"
        statement = statement.where(
            db.or_(
                Event.title.ilike(pattern),
                Event.description.ilike(pattern),
                Event.location.ilike(pattern),
                Event.venue_name.ilike(pattern),
                Category.name.ilike(pattern)
            )
        )

    events = db.session.scalars(statement).all()
    events.sort(key=lambda event: get_keyword_score(query, event), reverse=True)

    return events[:limit]


def get_events_by_creator(creator_id):
    return db.session.scalars(
        db.select(Event)
        .where(Event.creator_id == creator_id)
        .order_by(Event.event_date.desc())
    ).all()