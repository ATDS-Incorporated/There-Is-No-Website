#website
from flask import Flask, render_template, request, redirect, make_response
from db import init_db, find_user_by_credentials, get_file_by_id, get_all_messages

app = Flask(__name__)
init_db()

#logging
import logging
from logging.handlers import RotatingFileHandler

# Configure access logging
handler = RotatingFileHandler('access.log', maxBytes=100000, backupCount=3)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s %(message)s'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


@app.before_request
def log_request():
    app.logger.info(
        f'{request.remote_addr} {request.method} {request.path} '
        f'UA={request.user_agent.string[:60]}'
    )

# --- Public corporate pages (the "normal looking" site) ---

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# --- Employee portal ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # NOTE: when you add the SQL injection puzzle, swap this
        # for find_user_raw(username, password) in db.py
        user = find_user_by_credentials(username, password)

        if user:
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie('role', user['role'])
            return resp
        return render_template('login.html', error='Invalid credentials.')
    return render_template('login.html')


@app.route('/employee/dashboard')
def dashboard():
    messages = get_all_messages()
    return render_template('/employee/dashboard.html', messages=messages)


@app.route('/files/<int:file_id>')
def file_view(file_id):
    f = get_file_by_id(file_id)
    if not f:
        return render_template('404.html'), 404
    return render_template('file.html', file=f)


# --- Error handler ---

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)