<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, session, url_for, flash
from db import init_db, get_user

app = Flask(__name__)
# Development-only secret
app.secret_key = 'dev-local-secret'

# Ensure database and default user exist
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = get_user(username)
        # Note: plain-text passwords in this test project
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('public/login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('employee/dashboard.html', username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True)
=======
#website
from flask import Flask, render_template, request, redirect, make_response
from db import init_db, find_user_by_credentials, get_file_by_id, get_all_messages

app = Flask(__name__)
init_db()

#logging
import logging
from logging.handlers import RotatingFileHandler
from db import log_audit

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
            log_audit(username, 'LOGIN_SUCCESS')
            return resp
        else:
            log_audit(username, 'LOGIN_FAILED')
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
>>>>>>> eb040c6d018264a2f5ba2599840a4e92e797a3a3
