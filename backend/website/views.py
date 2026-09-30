from flask import Blueprint
from .services import get_all_events, get_event_by_id, get_tickets_remaining

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = get_all_events()

    return {
        'events': [
            {
                'id': event.id,
                'title': event.title,
                'price': float(event.price),
                'capacity': event.capacity
            }
            for event in events
        ]
    }

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

    