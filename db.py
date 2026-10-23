import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'game.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, sender TEXT, date TEXT, body TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY, owner TEXT, filename TEXT, content TEXT)''')

    # If no users exist yet, insert a default local test user
    c.execute('SELECT COUNT(*) FROM users')
    count = c.fetchone()[0]
    if count == 0:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                  ('admin', 'password', 'admin'))

    conn.commit()
    conn.close()


def get_user(username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return row
