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
