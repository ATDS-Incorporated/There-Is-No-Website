import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'game.db')


def get_db():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they do not exist. No data insertion."""
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id           INTEGER PRIMARY KEY,
        username     TEXT UNIQUE NOT NULL,
        password     TEXT NOT NULL,
        role         TEXT NOT NULL DEFAULT 'user',
        display_name TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id       INTEGER PRIMARY KEY,
        sender   TEXT NOT NULL,
        date     TEXT NOT NULL,
        body     TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id        INTEGER PRIMARY KEY,
        owner     TEXT NOT NULL,
        filename  TEXT NOT NULL,
        content   TEXT NOT NULL,
        is_secret INTEGER DEFAULT 0
    )''')

    conn.commit()
    conn.close()

def log_audit(actor, action, detail=''):
    conn = get_db()
    conn.execute(
        "INSERT INTO audit_log (timestamp, actor, action, detail) "
        "VALUES (datetime('now'), ?, ?, ?)",
        (actor, action, detail)
    )
    conn.commit()
    conn.close()


def get_audit_log(limit=50):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows

# Helper functions

def find_user_by_credentials(username, password):
    """Safe parameterized query. Use this everywhere except the SQLi puzzle."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    return user


def find_user_raw(username, password):
    """VULNERABLE — do not use outside the SQLi puzzle route."""
    conn = get_db()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()
    conn.close()
    return user


def get_file_by_id(file_id):
    conn = get_db()
    f = conn.execute("SELECT * FROM files WHERE id = ?", (file_id,)).fetchone()
    conn.close()
    return f


def get_all_messages():
    conn = get_db()
    msgs = conn.execute("SELECT * FROM messages ORDER BY date").fetchall()
    conn.close()
    return msgs


def db_is_seeded():
    conn = get_db()
    try:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    except sqlite3.OperationalError:
        count = 0
    conn.close()
    return count > 0