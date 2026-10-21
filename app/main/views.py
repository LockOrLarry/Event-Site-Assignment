from flask import abort, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from ..services import (
    get_all_events,
    get_all_categories,
    get_featured_events,
    get_event_by_id,
    get_tickets_remaining,
    create_booking,
    create_comment,
    get_bookings_by_user,
    get_events_by_creator,
    get_effective_event_status,
    create_event as save_event,
    search_events,
    keyword_search_events,
    update_event
)
from .forms import (
    BookingForm,
    CommentForm,
    EventCreationForm,
    EventEditForm
)
from . import main_bp
from .. import db
from ..models import Category
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

@main_bp.route('/')
def index():
    return render_template(
        'index.html',
        categories=get_all_categories(),
        featured=get_featured_events(),
        get_effective_event_status=get_effective_event_status
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
        comment_form=CommentForm(),
        effective_status=get_effective_event_status(event)
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
@login_required
def booking_history():
    bookings = get_bookings_by_user(current_user.id)

    return render_template(
        'booking-history.html',
        bookings=bookings
    )


@main_bp.route('/my-events/')
@login_required
def my_events():
    events = get_events_by_creator(current_user.id)

    print("CURRENT USER ID:", current_user.id)
    print("MY EVENT IDS:", [event.id for event in events])

    return render_template(
        'my-events.html',
        events=events,
        get_effective_event_status=get_effective_event_status,
        get_tickets_remaining=get_tickets_remaining
    )


@main_bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventCreationForm()

    categories = db.session.scalars(
        db.select(Category).order_by(Category.name)
    ).all()

    form.category_id.choices = [
        (category.id, category.name)
        for category in categories
    ]

    if form.validate_on_submit():
        image = form.image.data

        filename = secure_filename(image.filename)
        extension = Path(filename).suffix.lower()

        unique_filename = f"{uuid4().hex}{extension}"

        upload_folder = Path(
            current_app.config['EVENT_UPLOAD_FOLDER']
        )
        upload_folder.mkdir(parents=True, exist_ok=True)

        saved_file = upload_folder / unique_filename

        try:
            image.save(saved_file)

            image_path = f"img/events/{unique_filename}"

            event = save_event(
                creator_id=current_user.id,
                form=form,
                image_path=image_path
            )

        except (OSError, SQLAlchemyError):
            db.session.rollback()

            if saved_file.exists():
                saved_file.unlink()

            current_app.logger.exception(
                'Failed to create event'
            )

            flash(
                'Something went wrong while creating your event.',
                'danger'
            )

        else:
            flash(
                'Your event has been created successfully!',
                'success'
            )

            return redirect(
                url_for('main.event_detail', event_id=event.id)
            )

    return render_template(
        'create-event.html',
        form=form
    )


@main_bp.route('/events/<int:event_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        abort(404)

    if event.creator_id != current_user.id:
        abort(403)

    if get_effective_event_status(event) == 'Completed':
        abort(403)

    form = EventEditForm()

    categories = db.session.scalars(
        db.select(Category).order_by(Category.name)
    ).all()

    form.category_id.choices = [
        (category.id, category.name)
        for category in categories
    ]

    if request.method == 'GET':
        form.title.data = event.title
        form.category_id.data = event.category_id
        form.description.data = event.description

        form.event_date.data = event.event_date.date()
        form.start_time.data = event.event_date.time()
        form.end_time.data = event.end_time

        form.venue_name.data = event.venue_name
        form.address.data = event.address
        form.suburb.data = event.suburb
        form.state.data = event.state
        form.postcode.data = event.postcode

        form.price.data = event.price
        form.capacity.data = event.capacity

        form.age_suitability.data = event.age_suitability
        form.dietary_options.data = event.dietary_options
        form.additional_details.data = event.additional_details

        form.acknowledgement_type.data = event.acknowledgement_type
        form.acknowledgement_text.data = event.acknowledgement_text

    if form.validate_on_submit():
        image = form.image.data
        image_path = None
        saved_file = None

        if image and image.filename:
            filename = secure_filename(image.filename)
            extension = Path(filename).suffix.lower()
            unique_filename = f"{uuid4().hex}{extension}"

            upload_folder = Path(
                current_app.config['EVENT_UPLOAD_FOLDER']
            )
            upload_folder.mkdir(parents=True, exist_ok=True)

            saved_file = upload_folder / unique_filename
            image_path = f"img/events/{unique_filename}"

        try:
            if saved_file is not None:
                image.save(saved_file)

            error = update_event(
                event,
                form,
                image_path=image_path
            )

            if error:
                if saved_file is not None and saved_file.exists():
                    saved_file.unlink()

                flash(error, 'danger')
            else:
                flash('Event updated successfully!', 'success')
                return redirect(
                    url_for('main.event_detail', event_id=event.id)
                )

        except (OSError, SQLAlchemyError, ValueError):
            db.session.rollback()

            if saved_file is not None and saved_file.exists():
                saved_file.unlink()

            current_app.logger.exception('Failed to update event')
            flash('Could not update the event.', 'danger')

    return render_template(
        'edit-event.html',
        form=form,
        event=event
    )
    

@main_bp.route('/search/')
def search():
    query = request.args.get('q', '').strip()
    mode = request.args.get('mode', 'smart')

    if not query:
        return redirect(url_for('main.index'))

    if mode == 'keyword':
        events = keyword_search_events(query)
    else:
        mode = 'smart'
        events = search_events(query)

    return render_template(
        'search.html',
        query=query,
        mode=mode,
        events=events,
        get_effective_event_status=get_effective_event_status
    )

