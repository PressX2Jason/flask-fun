import pytest
from flask import g, session
from flaskr.db import get_db
from flaskr.auth import validate_api_key


def test_register(client, app):
    validEmail = 'a@live.com'
    response = client.post(
        '/register', data={'email': validEmail, 'password': 'a'}
    )
    assert response.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "select * from user where email = ?", (validEmail, )
        ).fetchone() is not None


@pytest.mark.parametrize(('email', 'password', 'message', 'httpStatusCode'), (
    ('', '', b'Email is required.', 400),
    ('a', '', b'Password is required.', 400),
    ('other@yahoo.com', 'test', b'already registered', 400),
))
def test_register_validate_input(client, email, password, message, httpStatusCode):
    response = client.post(
        '/register',
        data={'email': email, 'password': password}
    )
    assert message in response.data
    assert httpStatusCode == response.status_code


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
