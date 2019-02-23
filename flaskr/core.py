import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import loginRequired

bp = Blueprint('core', __name__)

@bp.route('/next', methods=('GET'))
@loginRequired
def get_next_seq():
    db = get_db()

    email = request.form['email']

    db.execute('UPDATE user SET curr_num = curr_num + 1 WHERE email = ?', (email, ))
    db.commit()
    count = db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ), one=True)
    return count
    
@bp.route('/current', methods=('GET'))
@loginRequired
def get_current_seq():
    db = get_db()
    errors = []

     email = request.form['email']

    count = db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ), one=True)
    return count