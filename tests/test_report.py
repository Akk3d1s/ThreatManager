import pytest
from app import app
from flask import url_for
import io
import flask_login
from app.models.user import User

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

def report(client, data):
    return client.post('/report', content_type='multipart/form-data', data=data, follow_redirects=True)

def test_successful_report_single_file(client):
    '''Test successful report'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(title='title', description='description', reproduce_steps='reproduce_steps', file=(io.BytesIO(b'file contents'), "filename.jpg"))
    rv = report(client, data)
    assert b'Report New Threat' in rv.data

def test_successful_report_multiple_files(client):
    '''Test successful report'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(title='title', description='description', reproduce_steps='reproduce_steps', file=[(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg")])
    rv = report(client, data)
    assert b'Report New Threat' in rv.data

def test_failed_report_unauthorized_role(client):
    '''Test unauthorized user report''' 
    with client.session_transaction() as session:
        session['_user_id'] = '4'
    data = dict(title='title', description='description', reproduce_steps='reproduce_steps', file=(io.BytesIO(b'file contents'), "filename.jpg"))
    rv = report(client, data)
    assert b'Dashboard' in rv.data

def test_failed_report_no_description(client):
    '''Test failed report with no description'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(title='title', description='', reproduce_steps='steps', file=(io.BytesIO(b'file contents'), "filename.jpg"))
    rv = report(client, data)
    assert b'Check this box to confirm that you are happy to send this issue to the Police' in rv.data

def test_failed_report_no_file(client):
    '''Test failed report with no file'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(title='title', description='description', reproduce_steps='steps')
    rv = report(client, data)
    assert b'Check this box to confirm that you are happy to send this issue to the Police' in rv.data

def test_failed_report_incorrect_file_extension(client):
    '''Test failed report with incorrect file extension (.exe)'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(title='title', description='description', reproduce_steps='steps', file=(io.BytesIO(b'file contents'), "filename.exe"))
    rv = report(client, data)
    assert b'Check this box to confirm that you are happy to send this issue to the Police' in rv.data

def test_failed_report_oversize_files(client):
    '''Test failed report with files over size limit (10mb)'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    data = dict(title='title', description='description', reproduce_steps='steps', file=[(io.BytesIO(b'file contents'*(1024**2)), "filename.jpg"),(io.BytesIO(b'file contents'*(1024**2)), "filename.jpg")])
    rv = report(client, data)
    assert b'Check this box to confirm that you are happy to send this issue to the Police' in rv.data

def test_failed_report_exceed_file_amount(client):
    '''Test failed report with over 20 files limit'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    files = [(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg"),(io.BytesIO(b'file contents'), "filename.jpg")]
    data = dict(title='title', description='description', reproduce_steps='steps', file=files)
    rv = report(client, data)
    assert b'Check this box to confirm that you are happy to send this issue to the Police' in rv.data

