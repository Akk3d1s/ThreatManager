import pytest
import pyotp
from app import app, url_safe_timed_serializer, max_confirmation_waiting_time, max_confirmation_resend_waiting_time
from app.models.user import User
from app.helpers.mailer import Mailer


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

def test_valid_registration(client, monkeypatch):
    '''Test valid registration'''
    first_name = 'first_name'
    surname = 'surname'
    email = 'email@test.com'
    password = 'Adm!n123'
    password2 = 'Adm!n123'
    secret = 'secret'
    totp = '123'

    logout(client)

    # TOPT should return True
    def mockreturn(param1, param2):
        return True
    monkeypatch.setattr(pyotp.TOTP, 'verify', mockreturn)

    rv = register(client, first_name, surname, email, password, password2, secret, totp)
    user = User.query.filter_by(email=email).first()
    assert user.email == email
    # cleanup
    user.delete()

def test_already_logged_in(client):
    '''Test already logged in'''

    logout(client)

    with client.session_transaction() as sess:
        sess['_fresh'] = True
        sess['_id'] = '123'
        sess['_user_id'] = '1'
        sess['login_attempts'] = 0

    rv = client.get('/register', follow_redirects=True)
    assert 'Logout' in rv.get_data(as_text=True)


def test_confirm_account(client, monkeypatch):
    '''Test confirming account'''

    logout(client)

    # Token validation should return true
    def mockreturn(token, max_age):
        return 'admin@police.com'
    monkeypatch.setattr(url_safe_timed_serializer, 'loads', mockreturn)

    rv = client.get('/confirm_account/123', follow_redirects=True)
    print(rv.get_data(as_text=True))
    assert 'Account already activated. Please login' in rv.get_data(as_text=True)

def test_confirm_account_with_invalid_account(client, monkeypatch):
    '''Test confirming account with invalid account'''

    logout(client)

    # Token validation should return true
    def mockreturn(token, max_age):
        return 'test@police.com'
    monkeypatch.setattr(url_safe_timed_serializer, 'loads', mockreturn)

    rv = client.get('/confirm_account/123', follow_redirects=True)
    print(rv.get_data(as_text=True))
    assert 'Invalid request' in rv.get_data(as_text=True)


def test_confirm_account_activate_account(client, monkeypatch):
    '''Test confirming account and activate account'''

    logout(client)

    first_name = 'first_name'
    surname = 'surname'
    email = 'email@test.com'
    password = 'Adm!n123'
    password2 = 'Adm!n123'
    secret = 'secret'
    totp = '123'

    # TOPT should return True
    def topt_mockreturn(param1, param2):
        return True
    monkeypatch.setattr(pyotp.TOTP, 'verify', topt_mockreturn)

    rv = register(client, first_name, surname, email, password, password2, secret, totp)

    # Token validation should return true
    def extract_email_mockreturn(token, max_age):
        return email
    monkeypatch.setattr(url_safe_timed_serializer, 'loads', extract_email_mockreturn)

    rv = client.get('/confirm_account/123', follow_redirects=True)
    print(rv.get_data(as_text=True))
    assert 'Congratulations, your account is now active!' in rv.get_data(as_text=True)
    user = User.query.filter_by(email=email).first()
    assert user.email == email
    # cleanup
    user.delete()


def test_resend_confirmation(client, monkeypatch):
    '''Test resending confirmation mail'''
    logout(client)

    def extract_email_mockreturn(token, max_age):
        return 'admin@police.com'
    monkeypatch.setattr(url_safe_timed_serializer, 'loads', extract_email_mockreturn)

    def send_email_mockreturn(email, confirmation_token):
        return True
    monkeypatch.setattr(Mailer, 'send_confirmation_mail', send_email_mockreturn)

    rv = client.get('/resend_confirmation/123', follow_redirects=True)
    assert 'Mail sent!' in rv.get_data(as_text=True)

def register(client, first_name, surname, email, password, password2, secret, totp):
    return client.post('/register', data=dict(first_name=first_name, surname=surname, email=email, password=password, password2=password2, secret=secret, totp=totp), follow_redirects=True)

def logout(client):
    return client.get('logout', follow_redirects=True)