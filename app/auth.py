import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Nie podano nazwy.'
        elif not password:
            error = 'Nie podano hasła.'
        elif execute_fetchone(
            f"SELECT id FROM users WHERE username = '{username}' "
        ) is not None:
            error = f'Użytkownik {username} już jest zarejestrowany.'

        if error is None:
            insert(
                f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
            )
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = execute_fetchone(
            f"SELECT * FROM users WHERE username = '{username}'"
        )

        if user is None:
            error = 'Incorrect username.'
        elif user[2] != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        tmp = execute_fetchone(
            f"SELECT * FROM users WHERE id = '{user_id}' "
        )
        g.user = {
            'id': tmp[0],
            'username': tmp[1]
        }
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view