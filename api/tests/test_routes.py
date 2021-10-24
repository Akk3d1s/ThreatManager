import pytest
import base64
from app import app
from flask import jsonify, request, make_response, send_from_directory

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

def test_successful_login(client):
    '''Test successful login'''
    username = 'developer@police.com'
    password = 'developer'

    rv = login(client, username, password)

    assert 'token' in rv.get_data(as_text=True)

def test_failed_login(client):
    '''Test successful login'''
    username = 'test@police.com'
    password = 'test'

    rv = login(client, username, password)

    assert 'Invalid credentials' in rv.get_data(as_text=True)

def login(client, username, password):
    return client.get('/login', headers={'Authorization': 'Basic {}'.format(base64.b64encode(bytes(username + ':' + password, encoding='raw_unicode_escape')).decode('utf8'))})