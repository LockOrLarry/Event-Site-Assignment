import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "instance" / "sitedata.sqlite"

NEW_COLUMNS = {
    "end_time": "TIME NOT NULL DEFAULT '23:59:00'",
    "venue_name": "VARCHAR(100) NOT NULL DEFAULT 'Venue not specified'",
    "address": "VARCHAR(150) NOT NULL DEFAULT 'Address not specified'",
    "suburb": "VARCHAR(100) NOT NULL DEFAULT 'Unknown'",
    "state": "VARCHAR(3) NOT NULL DEFAULT 'QLD'",
    "postcode": "VARCHAR(4) NOT NULL DEFAULT '0000'",
    "age_suitability": "VARCHAR(20) NOT NULL DEFAULT 'All Ages'",
    "dietary_options": "VARCHAR(50) NOT NULL DEFAULT 'Multiple dietary options'",
    "additional_details": "TEXT",
}


def migrate():
    if not DATABASE.is_file():
        print(f"Database not found: {DATABASE}")
        print("No changes made.")
        return

    with sqlite3.connect(DATABASE) as connection:
        existing_columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(event)")
        }

        if not existing_columns:
            print("Event table not found. No changes made.")
            return

        for column, definition in NEW_COLUMNS.items():
            if column in existing_columns:
                print(f"Already exists: {column}")
                continue

            connection.execute(
                f"ALTER TABLE event ADD COLUMN {column} {definition}"
            )
            print(f"Added: {column}")

        connection.commit()

    print("Event database migration completed.")


if __name__ == "__main__":
    migrate()
