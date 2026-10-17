from app import create_app, db
from app.models import User, Category, Event, Booking, Comment
from datetime import datetime, timedelta
from app.services import update_event_embedding

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

    user3 = User(
        first_name='Emily',
        surname='Nguyen',
        email='emily@example.com',
        password_hash='dummy_hash_3',
        phone='0434567890',
        address='15 Edward Street, Brisbane'
    )

    category1 = Category(
        name='Food Festivals',
        description='Festivals celebrating food, drinks, and culture.'
    )

    category2 = Category(
        name='Dining Experiences',
        description='Unique dining events that offer memorable culinary experiences.'
    )

    category3 = Category(
        name='Cooking Workshops',
        description='Workshops focused on teaching new cooking skills.'
    )

    category4 = Category(
        name='Tastings',
        description='Tasting events for food and beverages.'
    )

    category5 = Category(
        name='Cultural Food Events',
        description='Events celebrating food from different cultures and regions.'
    )

    db.session.add_all([
        user1,
        user2,
        user3,
        category1,
        category2,
        category3,
        category4,
        category5
    ])

    db.session.commit()

    event1 = Event(
        creator_id=user1.id,
        category_id=category1.id,
        title='Brisbane Street Food Festival',
        description="Brisbane Street Food Festival brings together some of the city's favourite food trucks, independent vendors and local chefs for an evening dedicated to great food and community.",
        event_date=datetime(2026, 11, 12, 16, 0),
        location='South Bank',
        price=25.00,
        capacity=500,
        image_path='img/Night-Feast.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event2 = Event(
        creator_id=user2.id,
        category_id=category1.id,
        title='Riverside Food & Wine Festival',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 19, 12, 0),
        location='Kangaroo Point',
        price=35.00,
        capacity=400,
        image_path='img/Riverside Food and Wine.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event3 = Event(
        creator_id=user1.id,
        category_id=category1.id,
        title='Brisbane Vegan Food Festival',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 26, 10, 0),
        location='West End',
        price=18.00,
        capacity=300,
        image_path='img/Vegan Food Festival.webp',
        status='Inactive',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event4 = Event(
        creator_id=user2.id,
        category_id=category1.id,
        title='Night Noodle Markets',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 3, 17, 0),
        location='South Bank',
        price=15.00,
        capacity=600,
        image_path='img/Night Noodle Markets.webp',
        status='Cancelled',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event5 = Event(
        creator_id=user1.id,
        category_id=category2.id,
        title='Japanese Omakase Night',
        description='Placeholder text.',
        event_date=datetime(2026, 9, 8, 19, 0),
        location='Brisbane CBD',
        price=120.00,
        capacity=12,
        image_path='img/Japanese Omakese Night.webp',
        status='Sold Out',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event6 = Event(
        creator_id=user2.id,
        category_id=category2.id,
        title='Rooftop Italian Dinner',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 24, 18, 30),
        location='Fortitude Valley',
        price=85.00,
        capacity=60,
        image_path='img/Rooftop Italian Dinner.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event7 = Event(
        creator_id=user1.id,
        category_id=category2.id,
        title='Candlelight French Dining',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 2, 19, 0),
        location='New Farm',
        price=110.00,
        capacity=40,
        image_path='img/CandleLight French Dining.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event8 = Event(
        creator_id=user2.id,
        category_id=category2.id,
        title="Chef's Table Experience",
        description='Placeholder text.',
        event_date=datetime(2026, 11, 9, 18, 30),
        location='South Brisbane',
        price=145.00,
        capacity=10,
        image_path='img/dining-experience.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event9 = Event(
        creator_id=user1.id,
        category_id=category3.id,
        title='Handmade Pasta Workshop',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 20, 10, 0),
        location='West End',
        price=65.00,
        capacity=16,
        image_path='img/Handmade Pasta Workshop.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event10 = Event(
        creator_id=user2.id,
        category_id=category3.id,
        title='Sushi Making Masterclass',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 27, 13, 0),
        location='Brisbane CBD',
        price=75.00,
        capacity=14,
        image_path='img/Sushi Making Masterclass.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event11 = Event(
        creator_id=user1.id,
        category_id=category3.id,
        title='Artisan Pizza Workshop',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 4, 11, 0),
        location='Newstead',
        price=60.00,
        capacity=18,
        image_path='img/Artisan Pizza Workshop.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event12 = Event(
        creator_id=user2.id,
        category_id=category3.id,
        title='French Pastry Class',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 11, 9, 30),
        location='Paddington',
        price=70.00,
        capacity=12,
        image_path='img/Pastry Class.webp',
        status='Sold Out',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event13 = Event(
        creator_id=user1.id,
        category_id=category4.id,
        title='Artisan Chocolate Tasting',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 25, 15, 0),
        location='New Farm',
        price=45.00,
        capacity=30,
        image_path='img/Artisan Chocolate Tasting.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event14 = Event(
        creator_id=user2.id,
        category_id=category4.id,
        title='Australian Wine Discovery',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 1, 18, 0),
        location='Brisbane CBD',
        price=65.00,
        capacity=40,
        image_path='img/Australian Wine Discovery.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event15 = Event(
        creator_id=user1.id,
        category_id=category4.id,
        title='Specialty Coffee Tasting',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 8, 9, 0),
        location='West End',
        price=35.00,
        capacity=20,
        image_path='img/Coffee Tasting.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event16 = Event(
        creator_id=user2.id,
        category_id=category4.id,
        title='Cheese & Wine Evening',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 14, 18, 30),
        location='Teneriffe',
        price=70.00,
        capacity=30,
        image_path='img/Cheese and Wine Dining.webp',
        status='Sold Out',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event17 = Event(
        creator_id=user1.id,
        category_id=category5.id,
        title='Moroccan Souk & Supper Night',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 27, 18, 0),
        location='Fortitude Valley',
        price=40.00,
        capacity=80,
        image_path='img/Moroccan Souk & Supper Night.webp',
        status='Inactive',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event18 = Event(
        creator_id=user2.id,
        category_id=category5.id,
        title='Japanese Matsuri Dinner',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 5, 17, 30),
        location='Brisbane CBD',
        price=55.00,
        capacity=100,
        image_path='img/Japanese Matsuri Dining.webp',
        status='Open',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event19 = Event(
        creator_id=user1.id,
        category_id=category5.id,
        title='Indian Diwali Feast',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 12, 18, 0),
        location='West End',
        price=48.00,
        capacity=120,
        image_path='img/indian-diwali-feast.webp',
        status='Inactive',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event20 = Event(
        creator_id=user2.id,
        category_id=category5.id,
        title='Korean Food & Culture Night',
        description='Placeholder text.',
        event_date=datetime(2026, 11, 19, 18, 0),
        location='Sunnybank',
        price=45.00,
        capacity=90,
        image_path='img/Korean Dining.webp',
        status='Cancelled',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    events = [
        event1,
        event2,
        event3,
        event4,
        event5,
        event6,
        event7,
        event8,
        event9,
        event10,
        event11,
        event12,
        event13,
        event14,
        event15,
        event16,
        event17,
        event18,
        event19,
        event20
        ]

    for event in events:
        event.end_time = (event.event_date + timedelta(hours=3)).time()
        event.venue_name = event.location
        event.address = event.location
        event.suburb = event.location
        event.state = 'QLD'
        event.postcode = '4000'

    db.session.add_all([
        event1,
        event2,
        event3,
        event4,
        event5,
        event6,
        event7,
        event8,
        event9,
        event10,
        event11,
        event12,
        event13,
        event14,
        event15,
        event16,
        event17,
        event18,
        event19,
        event20
    ])

    db.session.commit()

    for event in events:
        update_event_embedding(event)

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
        text='Went to this festival last year and loved the variety of food. Really looking forward to going again!',
        comment_date=datetime(2026, 8, 28, 14, 30)
    )

    comment2 = Comment(
        user_id=user1.id,
        event_id=event2.id,
        text='Fresh pasta sounds amazing. Excited for this event!',
        comment_date=datetime(2026, 8, 29, 10, 15)
    )

    comment3 = Comment(
        user_id=user3.id,
        event_id=event1.id,
        text='Does anyone know if there will be plenty of vegetarian options this year?',
        comment_date=datetime(2026, 8, 30, 9, 45)
    )

    comment4 = Comment(
        user_id=user1.id,
        event_id=event1.id,
        text='The location is perfect. South Bank in the evening should be amazing.',
        comment_date=datetime(2026, 8, 30, 11, 0)
    )

    db.session.add_all([
        booking1,
        booking2,
        comment1,
        comment2,
        comment3,
        comment4
    ])

    db.session.commit()