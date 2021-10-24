import pytest
from app import app
from app.helpers.logger import PATH_ACTION_LIST
from app.helpers.authenticator import UNAUTHORIZED_ROUTE_ACCESS
from app.helpers.id_validator import INVALID_ID_FLASH_LIST


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

def apply_new_case(client, threat_id=1):
    return client.post('/newcase_application/{}'.format(threat_id), follow_redirects=True)

def apply_end_case(client, threat_id=1):
    return client.post('/endcase_application/{}'.format(threat_id), follow_redirects=True)

def approve_new_case(client, threat_id=1, category_id=1):
    return client.post('/newcase_approve/{}/{}'.format(threat_id, category_id), follow_redirects=True)

def reject_new_case(client, threat_id=1):
    return client.post('/newcase_reject/{}'.format(threat_id), follow_redirects=True)

def approve_end_case(client, threat_id=1):
    return client.post('/endcase_approve/{}'.format(threat_id), follow_redirects=True)

def reject_end_case(client, threat_id=1):
    return client.post('/endcase_reject/{}'.format(threat_id), follow_redirects=True)


# Application for New or End case 
def test_successful_apply_new_case(client):
    '''Test successful new case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '2' # editor role user
    rv = apply_new_case(client)
    # assert b'Applied for New Case' in rv.data # action logger flash message
    assert PATH_ACTION_LIST['newcase_application'].encode() in rv.data # action logger flash message

def test_failed_apply_new_case_unauthorized_role(client):
    '''Test unauthorized user role for new case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    rv = apply_new_case(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_apply_new_case_invalid_threat_id(client):
    '''Test unsuccessful new case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    threat_id = 300
    rv = apply_new_case(client, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data

def test_successful_apply_end_case(client):
    '''Test successful end case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '2' # editor role user
    rv = apply_end_case(client)
    assert PATH_ACTION_LIST['endcase_application'].encode() in rv.data

def test_failed_apply_end_case_unauthorized_role(client):
    '''Test unauthorized user role for end case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    rv = apply_end_case(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_apply_end_case_invalid_threat_id(client):
    '''Test unsuccessful new case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    threat_id = 300
    rv = apply_end_case(client, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data


# Approving New or End Case
def test_successful_approve_new_case(client):
    '''Test successful approval of new case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # approver role user
    rv = approve_new_case(client)
    assert PATH_ACTION_LIST['newcase_approve'].encode() in rv.data

def test_failed_approve_new_case_unauthorized_role(client):
    '''Test unauthorized user role for approving new case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    rv = approve_new_case(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_approve_new_case_invalid_threat_id(client):
    '''Test unsuccessful approving new case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '3'
    threat_id = 300
    rv = approve_new_case(client, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data

def test_failed_approve_new_case_invalid_category_id(client):
    '''Test unsuccessful approving new case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '3'
    threat_id = 1
    category_id = 300
    rv = approve_new_case(client, threat_id, category_id)
    assert INVALID_ID_FLASH_LIST['category_id'].encode() in rv.data

def test_successful_approve_end_case(client):
    '''Test successful approval of end case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # approver role user
    rv = approve_end_case(client)
    assert PATH_ACTION_LIST['endcase_approve'].encode() in rv.data

def test_failed_approve_end_case_unauthorized_role(client):
    '''Test unauthorized user role for approving end case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    rv = approve_end_case(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_approve_end_case_invalid_threat_id(client):
    '''Test unsuccessful approving end case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '3'
    threat_id = 300
    rv = approve_end_case(client, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data


# Rejecting New or End Case
def test_successful_reject_new_case(client):
    '''Test successful rejection of new case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # approver role user
    rv = reject_new_case(client)
    assert PATH_ACTION_LIST['newcase_reject'].encode() in rv.data

def test_failed_reject_new_case_unauthorized_role(client):
    '''Test unauthorized user role for rejecting new case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    rv = reject_new_case(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_reject_new_case_invalid_threat_id(client):
    '''Test unsuccessful approving new case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '3'
    threat_id = 300
    rv = reject_new_case(client, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data

def test_successful_reject_end_case(client):
    '''Test successful rejection of end case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # approver role user
    rv = reject_end_case(client)
    assert PATH_ACTION_LIST['endcase_reject'].encode() in rv.data

def test_failed_reject_end_case_unauthorized_role(client):
    '''Test unauthorized user role for rejecting end case application'''
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    rv = reject_end_case(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_reject_end_case_invalid_threat_id(client):
    '''Test unsuccessful approving end case application due to invalid threat_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '3'
    threat_id = 300
    rv = reject_end_case(client, threat_id)
    assert INVALID_ID_FLASH_LIST['threat_id'].encode() in rv.data

