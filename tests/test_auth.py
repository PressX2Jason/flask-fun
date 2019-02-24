import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    response = client.post(
        '/register', data={'email': 'a', 'password': 'a'}
    )

    with app.app_context():
        assert get_db().execute(
            "select * from user where email = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'Email is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, email, password, message):
    response = client.post(
        '/register',
        data={'email': email, 'password': password}
    )
    assert message in response.data