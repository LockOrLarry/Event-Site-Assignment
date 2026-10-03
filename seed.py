from app import create_app, db
from app.models import User, Category, Event, Booking, Comment
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(
        first_name='Amir',
        surname='Karimov',
        email='amir@example.com',
        password_hash='dummy_hash_1',
        phone='0412345678',
        address='10 Queen Street, Brisbane'
    )

    user2 = User(
        first_name='Sofia',
        surname='Rossi',
        email='sofia@example.com',
        password_hash='dummy_hash_2',
        phone='0423456789',
        address='25 George Street, Brisbane'
    )

    category1 = Category(
        name='Central Asian Cuisine',
        description='Food events featuring Central Asian cuisine and traditions.'
    )

    category2 = Category(
        name='Italian Cuisine',
        description='Food events focused on Italian dishes and cooking techniques.'
    )

    category3 = Category(
        name='Baking',
        description='Workshops and events focused on baking and pastry making.'
    )

    db.session.add_all([
        user1,
        user2,
        category1,
        category2,
        category3
    ])

    db.session.commit()

    event1 = Event(
        creator_id=user1.id,
        category_id=category1.id,
        title='Uzbek Plov Workshop',
        description='Learn how to prepare traditional Uzbek plov in a hands-on cooking workshop.',
        event_date=datetime(2026, 10, 15, 18, 0),
        location='Brisbane City',
        price=35.00,
        capacity=20,
        image_path='images/plov-workshop.jpg',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event2 = Event(
        creator_id=user2.id,
        category_id=category2.id,
        title='Italian Pasta Masterclass',
        description='Learn how to make fresh pasta from scratch and prepare classic Italian dishes.',
        event_date=datetime(2026, 10, 22, 17, 30),
        location='South Bank, Brisbane',
        price=45.00,
        capacity=15,
        image_path='images/pasta-masterclass.jpg',
        status='Open',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event is held.'
    )

    event3 = Event(
        creator_id=user1.id,
        category_id=category3.id,
        title='Artisan Bread Workshop',
        description='A practical workshop covering the fundamentals of preparing and baking artisan bread.',
        event_date=datetime(2026, 11, 5, 10, 0),
        location='West End, Brisbane',
        price=30.00,
        capacity=12,
        image_path='images/bread-workshop.jpg',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    db.session.add_all([
        event1,
        event2,
        event3
    ])

    db.session.commit()

    booking1 = Booking(
        user_id=user2.id,
        event_id=event1.id,
        quantity=2,
        price=35.00
    )

    booking2 = Booking(
        user_id=user1.id,
        event_id=event2.id,
        quantity=1,
        price=45.00
    )

    comment1 = Comment(
        user_id=user2.id,
        event_id=event1.id,
        text='Looking forward to learning how to make plov!'
    )

    comment2 = Comment(
        user_id=user1.id,
        event_id=event2.id,
        text='Fresh pasta sounds amazing. Excited for this event!'
    )

    db.session.add_all([
        booking1,
        booking2,
        comment1,
        comment2
    ])

    db.session.commit()