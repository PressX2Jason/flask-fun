import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('core', __name__)

@bp.route('/next', methods=['GET'])
@login_required
def get_next_seq():
    db = get_db()

    email = request.form['email']

    db.execute('UPDATE user SET curr_num = curr_num + 1 WHERE email = ?', (email, ))
    db.commit()
    count = db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ), one=True)
    return count
    
@bp.route('/current', methods=['GET', 'PUT'])
@login_required
def current_seq():
    def get_current_seq(db, email):
        return {'current' : db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ), one=True)}

    def set_current_seq(db, email, newValue):
        db.execute('UPDATE user SET curr_num = ? WHERE email = ?', (email, newValue))
        db.commit()
        return get_current_seq(db, email)

    db = get_db()
    if request.method == 'GET':
        result = get_current_seq(db, request.form['email'])
    if request.method == 'PUT':
        result = set_current_seq(db, request.form['email'], request.form['current'])
    return result 