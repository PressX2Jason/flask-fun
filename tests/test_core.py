import pytest
from flask import g, session
from flaskr.db import get_db

def test_get_next_seq(client, app):

    response = client.get(
        '/register', data={'email': 'a', 'password': 'a'}
    )

    with app.app_context():
        assert get_db().execute(
            "select * from user where email = 'a'",
        ).fetchone() is not None