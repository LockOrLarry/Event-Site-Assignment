# Event Site (QUT IAB207 group assignment)

A Flask web app for finding, booking and running local events. Users can browse and search events, book tickets, comment, and create or edit their own listings.

Built by [Lachlan](https://github.com/LockOrLarry), [Timur](https://github.com/Timur778), and [Josh](https://github.com/joshXIXI) for QUT's IAB207 (Rapid Web Application Development) unit in 2026.

## Features

- **Accounts:** register, log in and log out (Flask-Login, passwords hashed with bcrypt)
- **Events:** create and edit listings with an image upload, venue and address, price, capacity, age suitability, dietary options and an optional Acknowledgement of Country
- **Bookings:** book tickets, with a check against remaining capacity. Events are marked Sold Out when the last ticket goes and Completed once they finish
- **Booking history** and a **My Events** page for organisers
- **Comments** on event pages
- **Search** across titles, categories and descriptions
- Only the person who created an event can edit it

## Search

The search was built in two parts. Keyword matching scores results by title, category and description. Alongside that, a Hugging Face sentence-transformer model turned each event description into an embedding and compared it with the query using cosine similarity, so plain-language searches like "something for kids on the weekend" still found relevant events.

The model is turned off in this public version to keep installs small and quick, so search runs on keywords only. The embedding and scoring code is still in `app/services.py` (`update_event_embedding` and `search_events`).

## Tech

Python, Flask, Flask-SQLAlchemy (SQLite), Flask-WTF / WTForms, Flask-Login, Flask-Bcrypt, Bootstrap 5 (Bootstrap-Flask), Jinja templates and custom CSS.

## Data model

`User`, `Event`, `Category`, `Booking` and `Comment`. A user can create many events, make many bookings and leave many comments. Each event belongs to one category.

## Running it locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py                   # creates the database with sample events
python main.py
```

Then open http://127.0.0.1:5000.

## Notes

This is coursework, so the secret key is hard-coded and debug mode is on. Both would change before any real deployment.
