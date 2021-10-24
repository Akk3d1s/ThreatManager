from _pytest.python_api import raises
import jwt
import pytest
import base64
from app import app
from flask import jsonify, request, make_response, send_from_directory
from app.models.threat import Threat

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

def test_threats(client, monkeypatch):
    '''Test retrieving threats'''
    mock_jwt(monkeypatch)
    rv = client.get('/threats?token=123')
    assert 'description' in rv.get_data(as_text=True)

def test_threats_error(client, monkeypatch):
    '''Test retrieving threats'''
    mock_jwt(monkeypatch)
    def mockreturn():
        return None

    monkeypatch.setattr(Threat, 'query', mockreturn)
    rv = client.get('/threats?token=123')
    assert 'error' in rv.get_data(as_text=True)

def test_files(client, monkeypatch):
    '''Test retrieving files'''
    mock_jwt(monkeypatch)
    rv = client.get('/threats/1/files?token=123')
    assert '[]' in rv.get_data(as_text=True)

def test_download(client, monkeypatch):
    '''Test downloading files'''
    mock_jwt(monkeypatch)
    rv = client.get('/threats/1/files/1/download?token=123')
    assert 'Unable to locate file' in rv.get_data(as_text=True)

def test_comments(client, monkeypatch):
    '''Test retrieving comments'''
    mock_jwt(monkeypatch)
    rv = client.get('/threats/1/comments?token=123')
    assert 'comment' in rv.get_data(as_text=True)


def login(client, username, password):
    return client.get('/login', headers={'Authorization': 'Basic {}'.format(base64.b64encode(bytes(username + ':' + password, encoding='raw_unicode_escape')).decode('utf8'))})

def mock_jwt(monkeypatch):
    def mockreturn(token, secret_key, algorithms):
        return {'user': 'developer@police.com'}
    monkeypatch.setattr(jwt, 'decode', mockreturn)