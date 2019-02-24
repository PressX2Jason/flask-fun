import pytest
from flask import g, session
from flaskr.db import get_db
from flaskr.auth import validate_api_key, validate_login


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

@pytest.mark.parametrize(('apiKey', 'result'), (
    ('NotAKey', 'Api Key is incorrect.'),
    ('key1', ''),
))
def test_validateApiKey(client, app, apiKey, result):

    with app.app_context():
        errors = validate_api_key(apiKey)
        if result:
            assert result in errors
        else:
            assert not errors


@pytest.mark.parametrize(('email', 'password', 'result'), (
    ('a', '', 'Email is incorrect.'),
    ('test', '', 'Password is incorrect.'),
))
def test_validateLogin(client, app, email, password, result):

    with app.app_context():
        errors = validate_login(email, password)
        if result:
            assert result in errors
        else:
            assert not errors
