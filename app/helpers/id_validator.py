"""Module that checks data ids"""
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
    """Validate the ids of different artifacts"""

    @staticmethod
    def validate_role_id(role_id):
        """Validate role id"""
        if not UserRole.query.filter_by(id=role_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['role_id'])
                return False
            except ValueError:
                return False
        return True

    @staticmethod
    def validate_threat_id_and_category_id(threat_id, category_id=1):
        """Validate threat and category ids"""
        if not Threat.query.filter_by(id=threat_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['threat_id'])
                return False
            except ValueError:
                return False
        if not ThreatCategory.query.filter_by(id=category_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['category_id'])
                return False
            except ValueError:
                return False
        return True

    @staticmethod
    def validate_role_application_id(role_application_id):
        """Validate role application id"""
        if not RoleApplication.query.filter_by(id=role_application_id).first():
            try:
                flash(INVALID_ID_FLASH_LIST['role_application_id'])
                return False
            except ValueError:
                return False
        return True
