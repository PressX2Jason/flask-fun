import pytest
from flask import g, session, json
from flaskr.headers import EMAIL_HEADER, API_KEY_HEADER, REQUEST_CURRENT

def _register_user(client, email, password):
    response = client.post(
        '/register', data={'email': email, 'password': password}
    )
    assert response.status_code == 200
    return response


def _get_pay_load(response, field):
    payload = json.loads(response.data)
    assert payload
    assert field in payload
    return payload[field]


def _get_current_req(client, email, apiKey, expectedHttpStatus=200):
    response = client.get(
        '/current', headers={EMAIL_HEADER: email, API_KEY_HEADER: apiKey})
    assert response
    assert response.status_code == expectedHttpStatus
    return response


def _put_current_req(client, email, apiKey, data, expectedHttpStatus=200):
    response = client.put(
        '/current', headers={EMAIL_HEADER: email, API_KEY_HEADER: apiKey}, data=data)
    assert response
    assert response.status_code == expectedHttpStatus
    return response


def _get_next_req(client, email, apiKey, expectedHttpStatus=200):
    response = client.get(
        '/next', headers={EMAIL_HEADER: email, API_KEY_HEADER: apiKey})
    assert response
    assert response.status_code == expectedHttpStatus
    return response


def test_happy_route(client, app):
    email = 'foobar@barfoo.com'
    password = 'hunter2'

    registerResponse = _register_user(client, email, password)

    apiKey = _get_pay_load(registerResponse, 'api_key')

    currentResponse = _get_current_req(client, email, apiKey)
    currentInt = _get_pay_load(currentResponse, 'current_int')
    assert currentInt == 0

    for i in range(1, 11):
        response = _get_next_req(client, email, apiKey)
        nextInt = _get_pay_load(response, 'next_int')
        assert nextInt == i

    for i in range(100, 150, 10):
        updatedCurrentResponse = _put_current_req(client, email, apiKey, {'current': i})
        reponseInt = _get_pay_load(updatedCurrentResponse, 'current_int')
        assert reponseInt == i

        currentResponse = _get_current_req(client, email, apiKey)
        currentInt = _get_pay_load(currentResponse, 'current_int')
        assert currentInt == i
