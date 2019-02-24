import pytest
from flask import g, session
from flaskr.db import get_db

test_user_header = {
    'X-Email':'test',
    'X-Api-Key':'key1'
}

def test_get_next_seq(client, app):

    response = client.get('/next', headers=test_user_header)
    print(response.data)
    assert response.status_code == 200
    assert response.data == b'{"next_int":1}\n'
