import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import loginRequired

bp = Blueprint('core', __name__)

@bp.route('/next', methods=['GET'])
@loginRequired
def get_next_seq():
    db = get_db()

    email = request.form['email']

    db.execute('UPDATE user SET curr_num = curr_num + 1 WHERE email = ?', (email, ))
    db.commit()
    count = db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ), one=True)
    return count
    
@bp.route('/current', methods=['GET', 'PUT'])
@loginRequired
def current_seq():
    def getCurrentSeq(db, email):
        return {'current' : db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ), one=True)}

    def setCurrentSeq(db, email, newValue):
        db.execute('UPDATE user SET curr_num = ? WHERE email = ?', (email, newValue))
        db.commit()
        return getCurrentSeq(db, email)

    db = get_db()
    if request.method == 'GET':
        result = getCurrentSeq(db, request.form['email'])
    if request.method == 'PUT':
        result = setCurrentSeq(db, request.form['email'], request.form['current'])
    return result 