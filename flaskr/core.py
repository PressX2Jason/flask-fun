import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import apiKey_required

bp = Blueprint('core', __name__)

@bp.route('/next', methods=['GET'])
@apiKey_required
def get_next_seq():
    db = get_db()
    email = request.headers['X-Email']

    db.execute('UPDATE user SET curr_num = curr_num + 1 WHERE email = ?', (email, ))
    db.commit()
    count = db.execute('SELECT curr_num FROM user WHERE email = ?', (email, )).fetchone()[0]
    return jsonify(next_int=count)
    
@bp.route('/current', methods=['GET', 'PUT'])
@apiKey_required
def current_seq():
    def get_current_seq(email):
        return db.execute('SELECT curr_num FROM user WHERE email = ?', (email, )).fetchone()[0]

    def set_current_seq(email, newValue):
        db.execute('UPDATE user SET curr_num = ? WHERE email = ?', (email, newValue))
        db.commit()
        return get_current_seq(email)

    db = get_db()
    if request.method == 'GET':
        result = get_current_seq(request.headers['X-Email'])
    if request.method == 'PUT':
        result = set_current_seq(request.headers['X-Email'], request.form['current'])
    return jsonify(current_int=result) 