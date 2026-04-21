import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

BASE_DIR = os.path.dirname(__file__)
# Prefer DB in the app root; if an existing DB was accidentally created inside the templates
# folder (from running the wrong script), use that DB to avoid data loss.
default_db = os.path.join(BASE_DIR, 'expenses.db')
alt_db = os.path.join(BASE_DIR, 'templates', 'expenses.db')
if os.path.exists(alt_db) and not os.path.exists(default_db):
    DB_PATH = alt_db
else:
    DB_PATH = default_db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')
    app.config['DATABASE'] = DB_PATH

    with app.app_context():
        init_db(app.config['DATABASE'])

    return app


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db(db_path: str):
    need_create = not os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if need_create:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        conn.commit()
    conn.close()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


app = create_app()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('Username and password are required.', 'warning')
            return render_template('register.html')
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                       (username, generate_password_hash(password)))
            db.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    user_id = session['user_id']
    expenses = db.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,)).fetchall()
    total = sum(row['amount'] for row in expenses) if expenses else 0.0
    # category summary
    cat_rows = db.execute('SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category', (user_id,)).fetchall()
    categories = {r['category']: r['total'] for r in cat_rows}
    return render_template('dashboard.html', expenses=expenses, total=total, categories=categories)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category'].strip()
        date = request.form['date']
        try:
            amt = float(amount)
        except ValueError:
            flash('Invalid amount', 'danger')
            return render_template('add_edit.html', expense=None)
        db = get_db()
        db.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)',
                   (session['user_id'], amt, category, date))
        db.commit()
        flash('Expense added.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_edit.html', expense=None)


@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    db = get_db()
    exp = db.execute('SELECT * FROM expenses WHERE id = ? AND user_id = ?', (expense_id, session['user_id'])).fetchone()
    if not exp:
        flash('Expense not found.', 'warning')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category'].strip()
        date = request.form['date']
        try:
            amt = float(amount)
        except ValueError:
            flash('Invalid amount', 'danger')
            return render_template('add_edit.html', expense=exp)
        db.execute('UPDATE expenses SET amount = ?, category = ?, date = ? WHERE id = ?', (amt, category, date, expense_id))
        db.commit()
        flash('Expense updated.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_edit.html', expense=exp)


@app.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    db = get_db()
    db.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, session['user_id']))
    db.commit()
    flash('Expense deleted.', 'info')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
