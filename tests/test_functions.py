import pytest
from app import app
from app.models.user_role import UserRole
from app.models.application_role import RoleApplication
from app.models.threat import Threat
from app.models.threat_category import ThreatCategory
from app.controllers.report import allowed_file
from app.helpers.id_validator import IdValidator
from app.helpers.authenticator import Authenticator
from tests.test_application_role import get_role_application_list
from sqlalchemy import desc

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
        yield client

# file upload function 
def test_allowed_file_valid():
    '''Test allowed extension'''
    assert allowed_file('file_name.jpeg') == True

def test_allowed_file_invalid():
    '''Test invalid extension'''
    assert allowed_file('file_name.exe') == False

# id validator functions
def test_validate_role_id_valid():
    '''Test valid role_id'''
    assert IdValidator.validate_role_id(UserRole.query.first().id) == True

def test_validate_role_id_invalid():
    '''Test invalid role_id'''
    invalid_id = UserRole.query.order_by(desc(UserRole.id)).first().id+1
    assert IdValidator.validate_role_id(invalid_id) == False

def test_validate_threat_id_valid():
    '''Test valid threat_id'''
    assert IdValidator.validate_threat_id_and_category_id(Threat.query.first().id) == True

def test_validate_threat_id_invalid():
    '''Test invalid threat_id'''
    invalid_id = Threat.query.order_by(desc(Threat.id)).first().id+1
    assert IdValidator.validate_threat_id_and_category_id(invalid_id) == False

def test_validate_category_id_valid():
    '''Test valid category_id'''
    assert IdValidator.validate_threat_id_and_category_id(Threat.query.first().id, ThreatCategory.query.first().id) == True

def test_validate_category_id_invalid():
    '''Test invalid category_id'''
    invalid_id = ThreatCategory.query.order_by(desc(ThreatCategory.id)).first().id+1
    assert IdValidator.validate_threat_id_and_category_id(Threat.query.first().id, invalid_id) == False

def test_validate_role_application_id_valid():
    '''Test valid role_application_id'''
    assert IdValidator.validate_role_application_id(RoleApplication.query.first().id) == True

def test_validate_role_application_id_invalid():
    '''Test invalid role_application_id'''
    invalid_id = RoleApplication.query.order_by(desc(RoleApplication.id)).first().id+1
    assert IdValidator.validate_role_application_id(invalid_id) == False

# authenticator functions
def test_authenticator_role_access_check_authorized(client):
    '''Test authorized role'''
    with client.session_transaction() as session:
        session['_user_id'] = '5' # admin role user
    get_role_application_list(client)
    assert Authenticator.role_access_check('/role_application_list') == True

def test_authenticator_role_access_check_unauthorized(client):
    '''Test authorized role'''
    with client.session_transaction() as session:
        session['_user_id'] = '3' # admin role user
    get_role_application_list(client)
    assert Authenticator.role_access_check('/role_application_list') == False

def test_authenticator_threat_access_check_authorized_citizen(client):
    '''Test authorized citizen for a threat'''
    with client.session_transaction() as session:
        session['_user_id'] = '1' # first seed citizen role user
    client.get('/threat') # for updating the current_user
    threat_id = 1
    assert Authenticator.citizen_access_check(threat_id) == True

def test_authenticator_threat_access_check_unauthorized_citizen(client):
    '''Test unauthorized citizen for a threat'''
    with client.session_transaction() as session:
        session['_user_id'] = '6' # another citizen role user
    client.get('/threat') # for updating the current_user
    threat_id = 1
    assert Authenticator.citizen_access_check(threat_id) == False

