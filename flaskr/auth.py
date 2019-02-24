import functools
from secrets import token_urlsafe

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__)
apiKeyLength = 40

# TODO: find a way to create API keys
def generate_api_key():
    return token_urlsafe()

@bp.route('/register', methods=['POST'])
def register():
    def email_exists(email):
        return db.execute('SELECT id FROM user WHERE email = ?', (email, ) ).fetchone() is not None

    email = request.form['email']
    password = request.form['password']
    db = get_db()
    errors = []

    if not email:
        errors.append('Email is required.')
    if not password:
        errors.append('Password is required.')
    if email and email_exists(email):
        errors.append('User {} is already registered.'.format(email))
    
    if not errors:
        api_key =  generate_api_key()
        db.execute(
            'INSERT INTO user (email, password, api_key, curr_num) values (?, ?, ?, ?)',
            (email, generate_password_hash(password), api_key, 0)
        )
        db.commit()
        return jsonify(api_key=api_key)

    return jsonify(errors=errors)

def validate_api_key(email, apiKey):
    errors = []
    db = get_db()

    apiKey = db.execute('SELECT * FROM user WHERE api_key = ?', (apiKey, )).fetchone()

    if apiKey is None:
        errors.append('Api Key is incorrect.')

    return errors

def apiKey_required(route):
    # TODO: check if we need both api key and password to access the api
    @functools.wraps(route)
    def wrapped_route(**kwargs):
        if request.headers:
            email = request.headers['X-Email'] 
            apiKey = request.headers['X-Api-Key']
        else:
            email = request.form['email'] 
            apiKey = request.form['api_key']

        errors = validate_api_key(email, apiKey)
        if errors:
            return errors

        return route(**kwargs)
    
    return wrapped_route
