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
    errors = []


    email = request.form['email']
    password = request.form['password']
    apiKey = request.form['apiKey']

    count = db.execute('SELECT curr_num FROM user WHERE email = ?', (email, ))
    pass
    
@bp.route('/current', methods=('GET'))
@loginRequired
def get_current_seq():
    db = get_db()
    errors = []

    count = db.execute('')
    pass