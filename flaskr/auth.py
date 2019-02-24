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

@bp.route('/register', methods=['POST'])
def register():
    def emailExists(email):
        return db.execute('SELECT id FROM user WHERE email = ?', (email, ) ).fetchone() is not None

    email = request.form['email']
    password = request.form['password']
    db = get_db()
    errors = []

    if not email:
        errors.append('email is required.')
    if not password:
        errors.append('Password  is required.')
    if email and emailExists(email):
        errors.append('User {} is already registered.'.format(email))
    
    if not errors:
        api_key =  generate_api_key()
        db.execute(
            'INSERT INTO user (email, password) values (?, ?, ?, ?)',
            (email, generate_password_hash(password), api_key, 0)
        )
        db.commit()
        return {'api_key': api_key}

    return errors

def validateLogin(email, password):
    errors = []
    db = get_db()

    user = db.execute('SELECT * FROM user WHERE email = ?', (email, )).fetchone()

    if user is None:
        errors.append('email is incorrect.')
    elif not check_password_hash(user['password'], password):
        errors.append('Password is incorrect.')

    return errors

def validateApiKey(email, apiKey):
    errors = []
    db = get_db()

    user = db.execute('SELECT * FROM user WHERE email = ?', (email, )).fetchone()

    if user is None:
        errors.append('email is incorrect.')
    elif user['apiKey'] != apiKey:
        errors.append('Api Key is incorrect.')

    return errors

def loginRequired(func):

    def wrapper():
        email = request.form['email']
        password = request.form['password']
        apiKey = request.form['apiKey']

        errors = validateLogin(email, password)
        if errors:
            return errors

        errors = validateApiKey(email, apiKey)
        if errors:
            return errors

        func()
    
    return wrapper



