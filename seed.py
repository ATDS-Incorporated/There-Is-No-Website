"""
Run this once to populate the database with story data.
Usage: python seed.py
Idempotent — safe to run multiple times.
"""
from db import init_db, get_db, db_is_seeded


def seed():
    init_db()

    if db_is_seeded():
        print("Database already seeded. Nothing to do.")
        return

    conn = get_db()
    c = conn.cursor()

    # --- Users (weak passwords on purpose — 2017-era) ---
    users = [
        ('admin',   'supersecret', 'admin', 'Administrator'),
    ]
    c.executemany(
        "INSERT INTO users (username, password, role, display_name) VALUES (?, ?, ?, ?)",
        users
    )

    # --- Messages (story fragments) ---
    messages = [
    ]
    c.executemany(
        "INSERT INTO messages (sender, date, body) VALUES (?, ?, ?)",
        messages
    )

    # --- Files (for the IDOR puzzle) ---
    files = [
        ('guest',  'welcome.txt',       'Welcome to the Meridian Systems Website.', 0),
    ]
    c.executemany(
        "INSERT INTO files (owner, filename, content, is_secret) VALUES (?, ?, ?, ?)",
        files
    )

    conn.commit()
    conn.close()
    print("Database seeded successfully.")


if __name__ == '__main__':
    seed()