from flask import abort, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..services import get_all_events, get_all_categories, get_featured_events, get_event_by_id, get_tickets_remaining, create_booking, create_comment
from .forms import BookingForm, CommentForm

from . import main_bp

@main_bp.route('/')
def index():
    return render_template(
        'index.html',
        categories=get_all_categories(),
        featured=get_featured_events()
    )

MAX_TICKETS_PER_BOOKING = 5

@main_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        abort(404)

    tickets_remaining = get_tickets_remaining(event)

    return render_template(
        'event-details.html',
        event=event,
        tickets_remaining=tickets_remaining,
        max_quantity=min(MAX_TICKETS_PER_BOOKING, tickets_remaining),
        booking_form=BookingForm(),
        comment_form=CommentForm()
    )

@main_bp.route('/events/<int:event_id>/book', methods=['POST'])
@login_required
def book_event(event_id):
    event = get_event_by_id(event_id)
    if event is None:
        abort(404)

    form = BookingForm()

    if not form.validate_on_submit():
        flash('Please enter a valid number of tickets.', 'warning')
    elif form.quantity.data > MAX_TICKETS_PER_BOOKING:
        flash(f'You can only book a maximum of {MAX_TICKETS_PER_BOOKING} tickets per booking.', 'warning')
    else:
        booking, error = create_booking(current_user.id, event.id, form.quantity.data)
        if error:
            flash(error, 'warning')
        else:
            total = booking.quantity * booking.price
            flash(f'Booked {booking.quantity} ticket(s) for {event.title}. Total: ${total:.2f}', 'success')

    return redirect(url_for('main.event_detail', event_id=event.id))

@main_bp.route('/events/<int:event_id>/comment', methods=['POST'])
@login_required
def comment_event(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        abort(404)

    form = CommentForm()

    if form.validate_on_submit():
        comment, error = create_comment(current_user.id, event.id, form.text.data)
        if error:
            flash(error, 'danger')
        else:
            flash('Comment posted successfully.', 'success')
    else:
        for errors in form.errors.values():
            for error in errors:
                flash(error, 'danger')

    return redirect(url_for('main.event_detail', event_id=event.id, _anchor='comments'))

@main_bp.route('/history/')
def booking_history():
    return render_template('booking-history.html')

@main_bp.route('/create/')
def create_event():
    return render_template('create-event.html')

    