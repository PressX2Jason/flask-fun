import pytest
from flask import g, session
from flaskr.db import get_db

test_user_header = {
    'X-Email': 'test@gmail.com',
    'X-Api-Key': 'key1'
}

other_user_header = {
    'X-Email': 'other@yahoo.com',
    'X-Api-Key': 'key2'
}

invalid_email_header = {
    'X-Email': 'totallyAEmail',
    'X-Api-Key': 'key1'
}

invalid_apiKey_header = {
    'X-Email': 'test@gmail.com',
    'X-Api-Key': 'definatelyAKey'
}


@pytest.mark.parametrize(('header', 'message', 'expectedHttpStatusCode'), (
    (test_user_header, b'{"next_int":1}\n', 200),
    (other_user_header, b'{"next_int":6}\n', 200),
    (invalid_email_header, b'Email format is invalid.', 400),
    (invalid_apiKey_header, b'Api Key is incorrect.', 400)
))
def test_next_seq_is(client, header, message, expectedHttpStatusCode):
    response = client.get('/next', headers=header)
    assert response.status_code == expectedHttpStatusCode
    assert message in response.data


@pytest.mark.parametrize(('header', 'message', 'expectedHttpStatusCode'), (
    (test_user_header, b'{"current_int":0}\n', 200),
    (other_user_header, b'{"current_int":5}\n', 200),
    (invalid_email_header, b'Email format is invalid.', 400),
    (invalid_apiKey_header, b'Api Key is incorrect.', 400),
))
def test_get_current_seq(client, header, message, expectedHttpStatusCode):
    response = client.get('/current', headers=header)
    assert response.status_code == expectedHttpStatusCode
    assert message in response.data


current_data_to_100 = {'current': 100}
current_data_to_150 = {'current': 100}


@pytest.mark.parametrize(('header', 'message', 'expectedHttpStatusCode', 'data'), (
    (test_user_header, b'{"current_int":100}\n', 200, current_data_to_100),
    (other_user_header, b'{"current_int":150}\n', 200, current_data_to_150),
    (invalid_email_header, b'Email format is invalid.', 400, current_data_to_100),
    (invalid_apiKey_header, b'Api Key is incorrect.', 400, current_data_to_100)
))
def test_put_current_seq(client, header, message, expectedHttpStatusCode, data):
    response = client.put('/current', headers=header, data=data)
    assert response.status_code == expectedHttpStatusCode
    assert message in response.data
