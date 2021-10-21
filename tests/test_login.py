import pytest
from app import app
import pyotp


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client


def test_login(client, monkeypatch):
    '''Test successful login'''
    email = 'admin@police.com'
    password = 'admin'
    totp = '123'

    # TOPT should return True
    def mockreturn(param1, param2):
        return True
    monkeypatch.setattr(pyotp.TOTP, 'verify', mockreturn)

    rv = login(client, email, password, totp)
    assert b'Role Applications' in rv.data


def login(client, email, password, totp):
    return client.post('/login', data=dict(email=email, password=password, totp=totp), follow_redirects=True)