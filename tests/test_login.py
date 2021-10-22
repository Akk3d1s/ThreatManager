import pytest
import pyotp
from app import app
from app.models.user import User


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client


def test_already_logged_in(client, monkeypatch):
    '''Test already logged in'''

    with client.session_transaction() as sess:
        sess['_fresh'] = True
        sess['_id'] = '123'
        sess['_user_id'] = '1'
        sess['login_attempts'] = 0

    rv = login(client, None, None, None)
    assert 'Logout' in rv.get_data(as_text=True)


def test_successful_login(client, monkeypatch):
    '''Test successful login'''
    email = 'admin@police.com'
    password = 'admin'
    totp = '123'

    # TOPT should return True
    def mockreturn(param1, param2):
        return True
    monkeypatch.setattr(pyotp.TOTP, 'verify', mockreturn)

    rv = login(client, email, password, totp)
    assert 'Logout' in rv.get_data(as_text=True)


def test_failed_login_invalid_user(client):
    '''Test failed login, user doesnt exist'''
    email = 'test@mail.com'
    password = 'test'
    totp = '123'
    
    rv = login(client, email, password, totp)
    assert 'Invalid email, password or TOTP code.' in rv.get_data(as_text=True)

def test_failed_login_user_inactive(client, monkeypatch):
    '''Test failed login, user not yet activated'''
    email = 'admin@police.com'
    password = 'admin'
    totp = '123'

    user = User.query.filter_by(email=email).first()
    user.is_active = False
    user.save()

    # TOPT should return True
    def mockreturn(param1, param2):
        return True
    monkeypatch.setattr(pyotp.TOTP, 'verify', mockreturn)

    rv = login(client, email, password, totp)
    assert 'Please confirm account.' in rv.get_data(as_text=True)
    user.is_active = True
    user.save()


def login(client, email, password, totp):
    return client.post('/login', data=dict(email=email, password=password, totp=totp), follow_redirects=True)