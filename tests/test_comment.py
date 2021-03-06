import io
import pytest
from app import app
from app.helpers.logger import PATH_ACTION_LIST
from app.helpers.id_validator import INVALID_ID_FLASH_LIST
from app.helpers.authenticator import UNAUTHORIZED_ROUTE_ACCESS, UNAUTHORIZED_THREAT_ACCESS

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

def comment(client, data=dict(comment='default comment', file=(io.BytesIO(),'')), threat_id=1):
    return client.post('/comment/{}'.format(threat_id), content_type='multipart/form-data', data=data, follow_redirects=True)

def test_successful_comment_single_file(client):
    '''Test successful comment with one file'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    data = dict(comment='comment_test_single_file', file=(io.BytesIO(b'file contents'), "filename.jpg"))
    rv = comment(client, data)
    assert PATH_ACTION_LIST['comment'].encode() in rv.data

def test_successful_comment_multiple_file(client):
    '''Test successful comment with multiple files'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    data = dict(comment='comment_test_multiple_file', file=[(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg")])
    rv = comment(client, data)
    assert PATH_ACTION_LIST['comment'].encode() in rv.data

def test_successful_comment_without_file(client):
    '''Test successful comment without file'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    data = dict(comment='comment_test_without_file', file=(io.BytesIO(),''))
    rv = comment(client, data)
    assert PATH_ACTION_LIST['comment'].encode() in rv.data # using the flash message from action logger function to check

def test_failed_comment_unauthorized_role(client):
    '''Test unauthorized user role comment'''
    with client.session_transaction() as session:
        session['_user_id'] = '4' # developer role
    data = dict(comment='comment_test_unauthorized_role')
    rv = comment(client, data)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_comment_unauthorized_citizen(client):
    '''Test unauthorized user role comment'''
    with client.session_transaction() as session:
        session['_user_id'] = '6'
    data = dict(comment='comment_test_unauthorized_citizen')
    rv = comment(client, data)
    assert UNAUTHORIZED_THREAT_ACCESS.encode() in rv.data

def test_failed_invalid_threat_id(client):
    '''Test invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(comment='comment_test_invalid_threat_id')
    threat_id = 300
    rv = comment(client, data, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data

def test_failed_comment_no_comment(client):
    '''Test unauthorized user role comment'''
    with client.session_transaction() as session:
        session['_user_id'] = ''
    data = dict(comment='', file=(io.BytesIO(b'file contents'), "filename.jpg"))
    rv = comment(client, data)
    assert PATH_ACTION_LIST['comment'].encode() not in rv.data

def test_failed_incorrect_file_extension(client):
    '''Test successful comment'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    data = dict(comment='comment_test_incorrect_extension', file=[(io.BytesIO(b'file contents'), "filename.exe"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg")])
    rv = comment(client, data)
    assert b'Invalid file type' in rv.data

def test_failed_incorrect_oversize_files(client):
    '''Test successful comment'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    data = dict(comment='comment_test_oversize_files', file=[(io.BytesIO(b'file contents'*(1024**2)), "filename.png"),(io.BytesIO(b'file contents'), ("filename2.jpg"))])
    rv = comment(client, data)
    assert PATH_ACTION_LIST['comment'].encode() not in rv.data

def test_failed_incorrect_exceed_file_amount(client):
    '''Test successful comment'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    files = [(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg")]
    data = dict(comment='comment_test_exceed_file_amount', file=files)
    rv = comment(client, data)
    assert PATH_ACTION_LIST['comment'].encode() not in rv.data

