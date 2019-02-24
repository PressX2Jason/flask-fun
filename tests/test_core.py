import pytest
from flask import g, session
from flaskr.db import get_db

test_user_header = {
    'X-Email':'test',
    'X-Api-Key':'key1'
}

other_user_header = {
    'X-Email':'other',
    'X-Api-Key':'key2'
}

def _assert_next_seq_is(client, header, expectValue):
    response = client.get('/next', headers=header)
    assert response.status_code == 200
    assert response.data == b'{"next_int":%d}\n' % expectValue

def test_get_next_seq(client):
    _assert_next_seq_is(client, test_user_header, 1)
    _assert_next_seq_is(client, other_user_header, 6)

def _assert_current_seq(client, httpMethod, header, expectValue, data=None):
    response = httpMethod('/current', headers=header, data=data)
    assert response.status_code == 200
    assert response.data == b'{"current_int":%d}\n' % expectValue

def test_current_seq_get(client):
    _assert_current_seq(client, client.get, test_user_header, 0)
    _assert_current_seq(client, client.get, other_user_header, 5)

current_data_to_100 = { 'current' : 100 }

def test_current_seq_put(client):
    _assert_current_seq(client, client.put, test_user_header, 0, data=current_data_to_100)
    _assert_current_seq(client, client.put, other_user_header, 5, data=current_data_to_100)
