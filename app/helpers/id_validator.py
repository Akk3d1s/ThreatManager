from flask import flash
from app.models.user_role import UserRole
from app.models.application_role import RoleApplication
from app.models.threat import Threat
from app.models.threat_category import ThreatCategory

INVALID_ID_FLASH_LIST = {
    'role_id': "Invalid Role ID",
    'role_application_id': "Invalid Role Application ID",
    'threat_id': "Invalid Threat ID",
    'category_id': "Invalid Category ID"
}


class IdValidator:
    @staticmethod
    def validateRoleID(role_id):
        if not UserRole.query.filter_by(id=role_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['role_id'])
                return False
            except:
                return False
        return True
    
    @staticmethod
    def validateThreatIDnCategoryID(threat_id, category_id=1):
        if not Threat.query.filter_by(id=threat_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['threat_id'])
                return False
            except:
                return False
        if not ThreatCategory.query.filter_by(id=category_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['category_id'])
                return False
            except:
                return False
        return True

    @staticmethod
    def validateRoleApplicationID(role_application_id):
        if not RoleApplication.query.filter_by(id=role_application_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['role_application_id'])
                return False
            except:
                return False
        return True