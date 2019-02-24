import pytest
from flask import g, session
from flaskr.db import get_db
from flaskr.auth import validate_api_key


def test_register(client, app):
    response = client.post(
        '/register', data={'email': 'a', 'password': 'a'}
    )
    assert response.status_code == 200

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

@pytest.mark.parametrize(('email', 'apiKey', 'result'), (
    ('NotAEmail', 'NotAKey', 'Api Key is incorrect.'),
    ('test', 'key1', ''),
))
def test_validateApiKey(client, email, app, apiKey, result):
    with app.app_context():
        errors = validate_api_key(email, apiKey)
        if result:
            assert result in errors
        else:
            assert not errors

