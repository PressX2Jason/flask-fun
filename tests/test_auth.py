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

@pytest.mark.parametrize(('registeredEmail', 'registeredPassword', 'accessEmail', 'accessApiKey', 'result'), (
    ('a', 'b', 'c', '1234356', 'Email is incorrect.'),
    ('a', 'b', 'a', 'abcdefg', 'Api Key is incorrect.'),
    ('a', 'b', 'a', '1234356', ''),
))
def test_validateApiKey(client, app, registeredEmail, registeredPassword, accessEmail, accessApiKey, result):

    response = client.post(
        '/register', data={'email': registeredEmail, 'password': registeredPassword}
    )

    with app.app_context():
        errors = validate_api_key(accessEmail, accessApiKey)
        print(errors)
        if result:
            assert result in errors
        else:
            assert not errors


@pytest.mark.parametrize(('registeredEmail', 'registeredPassword', 'accessEmail', 'accessPassword', 'result'), (
    ('a', 'b', 'c', 'b', 'Email is incorrect.'),
    ('a', 'b', 'a', 'c', 'Password is incorrect.'),
    ('a', 'b', 'a', 'b', ''),
))
def test_validateLogin(client, app, registeredEmail, registeredPassword, accessEmail, accessPassword, result):

    response = client.post(
        '/register', data={'email': registeredEmail, 'password': registeredPassword}
    )

    with app.app_context():
        errors = validate_login(accessEmail, accessPassword)
        print(errors)
        if result:
            assert result in errors
        else:
            assert not errors
