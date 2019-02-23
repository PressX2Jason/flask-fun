import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('core', __name__, url_prefix='')

@bp.route('/next', methods=('GET'))
def get_next_seq():
    pass
    
@bp.route('/current', methods=('GET'))
def get_current_seq():
    pass