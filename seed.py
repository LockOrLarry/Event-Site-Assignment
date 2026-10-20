from app import create_app, db
from app.models import User, Category, Event, Booking, Comment
from datetime import datetime, timedelta, time
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
        end_time=time(22, 0),
        location='Stanley Street Plaza, South Brisbane, QLD 4101',
        venue_name='South Bank Parklands',
        address='Stanley Street Plaza',
        suburb='South Brisbane',
        state='QLD',
        postcode='4101',
        price=25.00,
        capacity=500,
        image_path='img/Night-Feast.webp',
        age_suitability='All Ages',
        dietary_options='Multiple dietary options',
        additional_details='Entry includes access to all stalls and live entertainment.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event2 = Event(
        creator_id=user2.id,
        category_id=category1.id,
        title='Riverside Food & Wine Festival',
        description="Riverside Food & Wine Festival brings together Queensland wineries, regional producers and local food vendors for an afternoon of tastings and waterfront dining at Kangaroo Point.",
        event_date=datetime(2026, 11, 19, 12, 0),
        end_time=time(18, 0),
        location='River Terrace, Kangaroo Point, QLD 4169',
        venue_name='Kangaroo Point Cliffs Park',
        address='River Terrace',
        suburb='Kangaroo Point',
        state='QLD',
        postcode='4169',
        price=35.00,
        capacity=400,
        image_path='img/Riverside Food and Wine.webp',
        age_suitability='18+',
        dietary_options='Vegetarian',
        additional_details='Ticket includes tasting access; full-sized meals and additional drinks are available for purchase.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land around the Brisbane River and Kangaroo Point, and pay our respects to Elders past and present.'
    )

    event3 = Event(
        creator_id=user1.id,
        category_id=category1.id,
        title='Brisbane Vegan Food Festival',
        description="Brisbane Vegan Food Festival showcases inventive plant-based meals, sustainable producers and dairy-free treats, bringing West End together for a day of fresh flavours and conscious food choices.",
        event_date=datetime(2026, 11, 26, 10, 0),
        end_time=time(16, 0),
        location='Boundary Street, West End, QLD 4101',
        venue_name='West End State School Community Grounds',
        address='Boundary Street',
        suburb='West End',
        state='QLD',
        postcode='4101',
        price=18.00,
        capacity=300,
        image_path='img/Vegan Food Festival.webp',
        age_suitability='All Ages',
        dietary_options='Vegan',
        additional_details='All listed food stalls serve plant-based options, with ingredient information available from individual vendors.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event4 = Event(
        creator_id=user2.id,
        category_id=category1.id,
        title='Night Noodle Markets',
        description="Night Noodle Markets brings South Bank to life with sizzling street food, handmade dumplings and aromatic noodle dishes, set among lively stalls and evening lights.",
        event_date=datetime(2026, 11, 3, 17, 0),
        end_time=time(22, 0),
        location='Clem Jones Promenade, South Brisbane, QLD 4101',
        venue_name='South Bank Parklands',
        address='Clem Jones Promenade',
        suburb='South Brisbane',
        state='QLD',
        postcode='4101',
        price=15.00,
        capacity=600,
        image_path='img/Night Noodle Markets.webp',
        age_suitability='All Ages',
        dietary_options='Multiple dietary options',
        additional_details='Entry provides access to the market area; food and drinks are purchased separately from vendors.',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event5 = Event(
        creator_id=user1.id,
        category_id=category2.id,
        title='Japanese Omakase Night',
        description="Japanese Omakase Night offers an intimate chef-led menu of seasonal Japanese dishes, highlighting carefully sourced ingredients, sushi craftsmanship and thoughtful presentation in the CBD.",
        event_date=datetime(2026, 9, 8, 19, 0),
        end_time=time(21, 30),
        location='Eagle Street, Brisbane City, QLD 4000',
        venue_name='Riverfront Dining Studio',
        address='Eagle Street',
        suburb='Brisbane City',
        state='QLD',
        postcode='4000',
        price=120.00,
        capacity=12,
        image_path='img/Japanese Omakese Night.webp',
        age_suitability='18+',
        dietary_options='No specific options',
        additional_details='A seated multi-course menu is served at a shared chef’s counter; please advise the organiser of allergies before attending.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land where this Brisbane City dining experience is held and pay our respects to Elders past and present.'
    )

    event6 = Event(
        creator_id=user2.id,
        category_id=category2.id,
        title='Rooftop Italian Dinner',
        description="Rooftop Italian Dinner pairs handmade pasta and regional Italian favourites with sweeping city views, offering a relaxed evening of seasonal food and warm hospitality in Fortitude Valley.",
        event_date=datetime(2026, 11, 24, 18, 30),
        end_time=time(21, 30),
        location='Wickham Street, Fortitude Valley, QLD 4006',
        venue_name='Valley Rooftop Kitchen',
        address='Wickham Street',
        suburb='Fortitude Valley',
        state='QLD',
        postcode='4006',
        price=85.00,
        capacity=60,
        image_path='img/Rooftop Italian Dinner.webp',
        age_suitability='18+',
        dietary_options='Vegetarian',
        additional_details='Ticket includes a shared Italian-inspired dinner; vegetarian meals can be requested when booking, subject to notice.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event7 = Event(
        creator_id=user1.id,
        category_id=category2.id,
        title='Candlelight French Dining',
        description="Candlelight French Dining brings classic French flavours to New Farm with a seasonal menu, considered wine pairings and an intimate candlelit setting for a memorable evening.",
        event_date=datetime(2026, 11, 2, 19, 0),
        end_time=time(21, 30),
        location='Brunswick Street, New Farm, QLD 4005',
        venue_name='Maison du Jardin',
        address='Brunswick Street',
        suburb='New Farm',
        state='QLD',
        postcode='4005',
        price=110.00,
        capacity=40,
        image_path='img/CandleLight French Dining.webp',
        age_suitability='18+',
        dietary_options='Multiple dietary options',
        additional_details='The evening features a set menu and optional wine pairing; dietary requests should be submitted before the event.',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event8 = Event(
        creator_id=user3.id,
        category_id=category2.id,
        title="Chef's Table Experience",
        description="Chef's Table Experience invites a small group to enjoy a creative multi-course dinner in South Brisbane, with seasonal ingredients and chefs sharing the inspiration behind each dish.",
        event_date=datetime(2026, 11, 9, 18, 30),
        end_time=time(21, 0),
        location='Grey Street, South Brisbane, QLD 4101',
        venue_name='Southside Test Kitchen',
        address='Grey Street',
        suburb='South Brisbane',
        state='QLD',
        postcode='4101',
        price=145.00,
        capacity=10,
        image_path='img/dining-experience.webp',
        age_suitability='18+',
        dietary_options='Multiple dietary options',
        additional_details='Includes a chef-designed tasting menu and conversation with the kitchen team; notify the organiser of dietary needs in advance.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land in South Brisbane and pay our respects to Elders past and present, recognising their continuing connection to Country.'
    )

    event9 = Event(
        creator_id=user1.id,
        category_id=category3.id,
        title='Handmade Pasta Workshop',
        description="Handmade Pasta Workshop teaches the fundamentals of fresh pasta, from mixing and kneading dough to shaping classic varieties and matching them with simple sauces in West End.",
        event_date=datetime(2026, 11, 20, 10, 0),
        end_time=time(13, 0),
        location='Vulture Street, West End, QLD 4101',
        venue_name='West End Cookery Studio',
        address='Vulture Street',
        suburb='West End',
        state='QLD',
        postcode='4101',
        price=65.00,
        capacity=16,
        image_path='img/Handmade Pasta Workshop.webp',
        age_suitability='13+',
        dietary_options='Vegetarian',
        additional_details='All equipment and ingredients are supplied, and participants prepare pasta to cook and enjoy during the session.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event10 = Event(
        creator_id=user2.id,
        category_id=category3.id,
        title='Sushi Making Masterclass',
        description="Sushi Making Masterclass introduces rice preparation, rolling techniques and balanced fillings in a practical Brisbane CBD session designed for curious cooks of all experience levels.",
        event_date=datetime(2026, 11, 27, 13, 0),
        end_time=time(15, 30),
        location='Queen Street, Brisbane City, QLD 4000',
        venue_name='City Culinary Workshop',
        address='Queen Street',
        suburb='Brisbane City',
        state='QLD',
        postcode='4000',
        price=75.00,
        capacity=14,
        image_path='img/Sushi Making Masterclass.webp',
        age_suitability='16+',
        dietary_options='Gluten-Free',
        additional_details='Ingredients and tools are provided, with a demonstration followed by hands-on practice; seafood handling is part of the class.',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event11 = Event(
        creator_id=user1.id,
        category_id=category3.id,
        title='Artisan Pizza Workshop',
        description="Artisan Pizza Workshop explores slow-fermented dough, fresh toppings and oven technique, giving participants practical skills to create crisp, flavourful pizzas in Newstead.",
        event_date=datetime(2026, 11, 4, 11, 0),
        end_time=time(14, 0),
        location='Commercial Road, Newstead, QLD 4006',
        venue_name='Newstead Pizza Lab',
        address='Commercial Road',
        suburb='Newstead',
        state='QLD',
        postcode='4006',
        price=60.00,
        capacity=18,
        image_path='img/Artisan Pizza Workshop.webp',
        age_suitability='13+',
        dietary_options='Vegetarian',
        additional_details='Participants make and bake their own pizza, with dough, toppings and cooking equipment provided for the workshop.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land in Newstead and pay our respects to Elders past and present.'
    )

    event12 = Event(
        creator_id=user2.id,
        category_id=category3.id,
        title='French Pastry Class',
        description="French Pastry Class explores the techniques behind buttery pastry and classic patisserie, guiding participants through careful preparation and baking in a Paddington kitchen.",
        event_date=datetime(2026, 11, 11, 9, 30),
        end_time=time(12, 30),
        location='Latrobe Terrace, Paddington, QLD 4064',
        venue_name='Paddington Baking Atelier',
        address='Latrobe Terrace',
        suburb='Paddington',
        state='QLD',
        postcode='4064',
        price=70.00,
        capacity=12,
        image_path='img/Pastry Class.webp',
        age_suitability='16+',
        dietary_options='Vegetarian',
        additional_details='The class covers pastry preparation and baking, with ingredients and takeaway boxes supplied for finished creations.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event13 = Event(
        creator_id=user1.id,
        category_id=category4.id,
        title='Artisan Chocolate Tasting',
        description="Artisan Chocolate Tasting explores premium chocolate through guided samples, revealing how cocoa origins, roasting and texture shape distinctive flavours in a relaxed New Farm setting.",
        event_date=datetime(2026, 11, 25, 15, 0),
        end_time=time(17, 0),
        location='Merthyr Road, New Farm, QLD 4005',
        venue_name='New Farm Chocolate Room',
        address='Merthyr Road',
        suburb='New Farm',
        state='QLD',
        postcode='4005',
        price=45.00,
        capacity=30,
        image_path='img/Artisan Chocolate Tasting.webp',
        age_suitability='13+',
        dietary_options='Gluten-Free',
        additional_details='The guided tasting includes several chocolate styles and notes on their origins; check with the organiser regarding allergens before booking.',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event14 = Event(
        creator_id=user2.id,
        category_id=category4.id,
        title='Australian Wine Discovery',
        description="Australian Wine Discovery samples distinctive wines from leading regions, pairing tasting notes with stories of local vineyards and winemaking traditions in Brisbane's city centre.",
        event_date=datetime(2026, 11, 1, 18, 0),
        end_time=time(20, 30),
        location='Edward Street, Brisbane City, QLD 4000',
        venue_name='City Wine Room',
        address='Edward Street',
        suburb='Brisbane City',
        state='QLD',
        postcode='4000',
        price=65.00,
        capacity=40,
        image_path='img/Australian Wine Discovery.webp',
        age_suitability='18+',
        dietary_options='Vegan',
        additional_details='Includes a guided tasting of selected Australian wines and tasting notes; non-alcoholic alternatives can be requested ahead of time.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land where this Brisbane City event takes place and pay our respects to Elders past and present.'
    )

    event15 = Event(
        creator_id=user3.id,
        category_id=category4.id,
        title='Specialty Coffee Tasting',
        description="Specialty Coffee Tasting celebrates West End's café culture with a guided look at carefully sourced beans, varied brewing methods and the flavours that distinguish each cup.",
        event_date=datetime(2026, 11, 8, 9, 0),
        end_time=time(11, 0),
        location='Boundary Street, West End, QLD 4101',
        venue_name='West End Coffee Workshop',
        address='Boundary Street',
        suburb='West End',
        state='QLD',
        postcode='4101',
        price=35.00,
        capacity=20,
        image_path='img/Coffee Tasting.webp',
        age_suitability='All Ages',
        dietary_options='Vegan',
        additional_details='Guests sample several coffees and learn basic tasting techniques; alternative milks are available for demonstration drinks.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event16 = Event(
        creator_id=user2.id,
        category_id=category4.id,
        title='Cheese & Wine Evening',
        description="Cheese & Wine Evening pairs artisan cheeses with selected wines in Teneriffe, offering a relaxed guided tasting of complementary flavours, textures and regional specialties.",
        event_date=datetime(2026, 11, 14, 18, 30),
        end_time=time(21, 0),
        location='Commercial Road, Teneriffe, QLD 4005',
        venue_name='Teneriffe Tasting Room',
        address='Commercial Road',
        suburb='Teneriffe',
        state='QLD',
        postcode='4005',
        price=70.00,
        capacity=30,
        image_path='img/Cheese and Wine Dining.webp',
        age_suitability='18+',
        dietary_options='Vegetarian',
        additional_details='Ticket includes a guided selection of cheese and wine pairings; guests should advise the organiser of dietary restrictions in advance.',
        acknowledgement_type='None',
        acknowledgement_text=None
    )

    event17 = Event(
        creator_id=user1.id,
        category_id=category5.id,
        title='Moroccan Souk & Supper Night',
        description="Moroccan Souk & Supper Night brings Fortitude Valley a lively evening of fragrant tagines, aromatic spices and market-inspired stalls, celebrating the hospitality and flavours of North Africa.",
        event_date=datetime(2026, 11, 27, 18, 0),
        end_time=time(21, 30),
        location='Brunswick Street, Fortitude Valley, QLD 4006',
        venue_name='Valley Courtyard Hall',
        address='Brunswick Street',
        suburb='Fortitude Valley',
        state='QLD',
        postcode='4006',
        price=40.00,
        capacity=80,
        image_path='img/Moroccan Souk & Supper Night.webp',
        age_suitability='All Ages',
        dietary_options='Vegan',
        additional_details='Entry includes a shared supper menu and access to themed market stalls; some stall purchases may cost extra.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land in Fortitude Valley and pay our respects to Elders past and present.'
    )

    event18 = Event(
        creator_id=user2.id,
        category_id=category5.id,
        title='Japanese Matsuri Dinner',
        description="Japanese Matsuri Dinner celebrates festival-inspired Japanese food with savoury street snacks, sweet treats and colourful decorations for a lively evening in Brisbane's CBD.",
        event_date=datetime(2026, 11, 5, 17, 30),
        end_time=time(21, 0),
        location='Albert Street, Brisbane City, QLD 4000',
        venue_name='City Festival Hall',
        address='Albert Street',
        suburb='Brisbane City',
        state='QLD',
        postcode='4000',
        price=55.00,
        capacity=100,
        image_path='img/Japanese Matsuri Dining.webp',
        age_suitability='All Ages',
        dietary_options='Multiple dietary options',
        additional_details='Ticket includes entry to the themed dining area; food stalls offer a rotating selection of dishes available for purchase.',
        acknowledgement_type='Generic',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respect to Elders past and present.'
    )

    event19 = Event(
        creator_id=user3.id,
        category_id=category5.id,
        title='Indian Diwali Feast',
        description="Indian Diwali Feast brings West End together over fragrant curries, freshly baked breads and traditional sweets, celebrating the festival of lights through food and community.",
        event_date=datetime(2026, 11, 12, 18, 0),
        end_time=time(21, 0),
        location='Vulture Street, West End, QLD 4101',
        venue_name='West End Community Hall',
        address='Vulture Street',
        suburb='West End',
        state='QLD',
        postcode='4101',
        price=48.00,
        capacity=120,
        image_path='img/indian-diwali-feast.webp',
        age_suitability='All Ages',
        dietary_options='Vegetarian',
        additional_details='A shared vegetarian-friendly feast is planned, with traditional sweets and non-alcoholic drinks available throughout the evening.',
        acknowledgement_type='Enhanced',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land in West End and pay our respects to Elders past and present as the community gathers to celebrate.'
    )

    event20 = Event(
        creator_id=user2.id,
        category_id=category5.id,
        title='Korean Food & Culture Night',
        description="Korean Food & Culture Night brings Sunnybank's food scene to life with Korean barbecue favourites, savoury pancakes and traditional side dishes alongside cultural activities.",
        event_date=datetime(2026, 11, 19, 18, 0),
        end_time=time(21, 0),
        location='Mains Road, Sunnybank, QLD 4109',
        venue_name='Sunnybank Cultural Centre',
        address='Mains Road',
        suburb='Sunnybank',
        state='QLD',
        postcode='4109',
        price=45.00,
        capacity=90,
        image_path='img/Korean Dining.webp',
        age_suitability='All Ages',
        dietary_options='Multiple dietary options',
        additional_details='The evening combines food stalls with introductory cultural activities; individual vendors can provide ingredient information on request.',
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