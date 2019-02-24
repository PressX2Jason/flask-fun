import functools
from secrets import token_urlsafe
from flaskr.email_validator import validate_email

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__)
apiKeyLength = 40


@bp.route('/register', methods=['POST'])
def register():
    def email_exists(email):
        return db.execute('SELECT id FROM user WHERE email = ?', (email, )).fetchone() is not None

    def register_new_email(email, password, apiKey):
        db.execute('INSERT INTO user (email, password, api_key, curr_num) values (?, ?, ?, ?)',
                   (email, generate_password_hash(password), apiKey, 0)
                   )
        db.commit()

    email = request.form['email']
    password = request.form['password']
    db = get_db()

    errors = validate_email(email)

    if not errors and email_exists(email):
        errors.append('User {} is already registered.'.format(email))
    if not password:
        errors.append('Password is required.')

    if errors:
        return jsonify(errors=errors), 400

    api_key = token_urlsafe()
    register_new_email(email, password, api_key)

    return jsonify(api_key=api_key)


def validate_api_key(email, apiKey):
    errors = []
    db = get_db()

    apiKey = db.execute(
        'SELECT * FROM user WHERE api_key = ?', (apiKey, )).fetchone()

    if apiKey is None:
        errors.append('Api Key is incorrect.')

    return errors


def apiKey_required(route):
    @functools.wraps(route)
    def wrapped_route(**kwargs):

        if request.headers:
            email = request.headers['X-Email']
            apiKey = request.headers['X-Api-Key']

        errors = validate_email(email)
        if not errors:
            errors = validate_api_key(email, apiKey)
        if errors:
            return jsonify(errors=errors), 400

        return route(**kwargs)

    return wrapped_route
