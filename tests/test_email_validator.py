import pytest
from flaskr.email_validator import validate_email



def test_validate_email_valid():
    errors = validate_email('test@google.ca')
    assert not errors

def test_validate_email_invalid():
    errors = validate_email('100%AnEmail')
    assert 'Email format is invalid.' in errors

def test_validate_email_empty():
    errors = validate_email('')
    assert 'Email is required.' in errors