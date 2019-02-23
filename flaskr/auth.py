import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# TODO: find a way to create API keys
def generate_api_key():
    return '1234356'

@bp.route('/next', methods=('GET'))
def get_next_in_seq():
    def usernameExists(username):
        return db.execute('SELECT id FROM user WHERE username = ?', (username, ) ).fetchone() is not None

    username = request.form['username']
    password = request.form['password']
    db = get_db()
    errors = []

    if not username:
        errors.append('Username is required.')
    if not password:
        errors.append('Password  is required.')
    if username and usernameExists(username):
        errors.append('User {} is already registered.'.format(username))
    
    if not errors:
        api_key =  generate_api_key()
        db.execute(
            'INSERT INTO user (username, password) values (?, ?, ?, ?)',
            (username, generate_password_hash(password), api_key, 0)
        )
        db.commit()
        return api_key
    
    if errors:
        flash(error)
    return 


