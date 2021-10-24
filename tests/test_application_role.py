import pytest
from app import app
from app.helpers.logger import PATH_ACTION_LIST
from app.helpers.authenticator import UNAUTHORIZED_ROUTE_ACCESS
from app.helpers.id_validator import INVALID_ID_FLASH_LIST
from app.models.application_role import RoleApplication


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

def apply_role_change(client, role_id):
    return client.post('/role_application/{}'.format(role_id), follow_redirects=True)

def get_role_application_list(client):
    return client.get('/role_application_list', follow_redirects=True)

def approve_role_change(client, application_id=1):
    return client.post('/role_application_approve/{}'.format(application_id), follow_redirects=True)

def reject_role_change(client, application_id=1):
    return client.post('/role_application_reject/{}'.format(application_id), follow_redirects=True)

# police roles applying for role change
def test_successful_apply_role_change(client):
    '''Test successful role change application'''
    with client.session_transaction() as session:
        session['_user_id'] = '2' # editor role user
    role_id = 3
    rv = apply_role_change(client, role_id)
    assert PATH_ACTION_LIST['role_application'].encode() in rv.data # action logger flash message

def test_failed_apply_role_change_unauthorized_role(client):
    '''Test unauthorized user role for role change applircation'''
    with client.session_transaction() as session:
        session['_user_id'] = '1' # citizen role user
    role_id = 3
    rv = apply_role_change(client, role_id)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_apply_role_change_invalid_role_id(client):
    '''Test failed role change application due to invalid role_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '2' # editor role user
    role_id = 300
    rv = apply_role_change(client, role_id)
    assert INVALID_ID_FLASH_LIST['role_id'].encode() in rv.data

def test_no_duplicated_role_application_for_one_user(client):
    '''Test weather duplicated role application for one user can exist'''
    with client.session_transaction() as session:
        session['_user_id'] = '2' # editor role user
    role_id = 4
    apply_role_change(client, role_id)
    role_id = 5
    apply_role_change(client, role_id)
    assert RoleApplication.query.filter(RoleApplication.user_id==2).count() == 1

# admin getting the list of role change application
def test_successful_get_role_application_list(client):
    '''Test successfully getting role change application list'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    rv = get_role_application_list(client)
    assert PATH_ACTION_LIST['role_application_list'].encode() in rv.data

def test_failed_get_role_application_list_unauthorized_role(client):
    '''Test failed in getting role change application list'''
    with client.session_transaction() as session:
        session['_user_id'] = '2'
    rv = get_role_application_list(client)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_successful_approve_role_change(client):
    '''Test successful approval of role change application'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    roleApplication = RoleApplication(user_id=2, role_id=4) # user2 is editor(3)
    roleApplication.save()
    rv = approve_role_change(client, roleApplication.id)
    assert PATH_ACTION_LIST['role_application_approve'].encode() in rv.data

# approve role change application
def test_successful_approve_role_change_back(client):
    '''Test successful approval of role change application'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    roleApplication = RoleApplication(user_id=2, role_id=3) # user2 is approver(4)
    roleApplication.save()
    rv = approve_role_change(client, roleApplication.id)
    assert PATH_ACTION_LIST['role_application_approve'].encode() in rv.data

def test_failed_approve_role_change_unauthorized_role(client):
    '''Test unauthorized user role for approving of role change application'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # editor role user
    roleApplication = RoleApplication(user_id=2, role_id=3) # user2 is approver(4)
    roleApplication.save()
    rv = approve_role_change(client, roleApplication.id)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_approve_role_change_invalid_application_id(client):
    '''Test failed approving role change application due to invalid application_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    role_application_id = 300
    rv = approve_role_change(client, role_application_id)
    assert INVALID_ID_FLASH_LIST['role_application_id'].encode() in rv.data

# reject role change application
def test_successful_reject_role_change_back(client):
    '''Test successful rejection of role change application'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    roleApplication = RoleApplication(user_id=2, role_id=3) # user2 is approver(4)
    roleApplication.save()
    rv = reject_role_change(client, roleApplication.id)
    assert PATH_ACTION_LIST['role_application_reject'].encode() in rv.data

def test_failed_reject_role_change_unauthorized_role(client):
    '''Test unauthorized user role for rejecting of role change application'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # editor role user
    roleApplication = RoleApplication(user_id=2, role_id=3) # user2 is approver(4)
    roleApplication.save()
    rv = reject_role_change(client, roleApplication.id)
    assert UNAUTHORIZED_ROUTE_ACCESS.encode() in rv.data

def test_failed_reject_role_change_invalid_application_id(client):
    '''Test failed rejecting role change application due to invalid application_id'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    role_application_id = 300
    rv = reject_role_change(client, role_application_id)
    assert INVALID_ID_FLASH_LIST['role_application_id'].encode() in rv.data

