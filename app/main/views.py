from flask import Blueprint, render_template
from ..services import get_all_events, get_event_by_id, get_tickets_remaining

from . import main_bp

@main_bp.route('/')
def index():
    events = get_all_events()

    return render_template('index.html', events=events)

@main_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        return {'error': 'Event not found'}, 404

    return {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.event_date.isoformat(),
        'location': event.location,
        'price': float(event.price),
        'capacity': event.capacity,
        'tickets_remaining': get_tickets_remaining(event),
        'status': event.status,
        'creator': event.creator.first_name,
        'category': event.category.name
    }

@main_bp.route('/history/')
def booking_history():
    return render_template('booking-history.html')

@main_bp.route('/create/')
def create_event():
    return render_template('create-event.html')

    