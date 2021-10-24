from flask import flash
from flask_login import current_user
from app.models.threat import Threat

# ROLE_LIST = {
#     'PUBLIC': 1,
#     'VIEWER': 2,
#     'EDITOR': 3,
#     'APPROVER': 4,
#     'DEVELOPER': 5,
#     'ADMIN': 6
# }
PATH_ROLE_LIST = {
    'api_credential': [5],
    'newcase_application': [3],
    'newcase_approve': [4],
    'newcase_reject': [4],
    'endcase_application': [3],
    'endcase_approve': [4],
    'endcase_reject': [4],
    'role_application': [2,3,4,5],
    'role_application_list': [6],
    'role_application_approve': [6],
    'role_application_reject': [6],
    'comment': [1,3,4],
    'download_file_threat': [1,2,3,4],
    'download_file_comment': [1,2,3,4],
    'download_all_cases_csv': [1,2,3,4],
    'report': [1,3]
}

UNAUTHORIZED_ROUTE_ACCESS = "Unauthorized Route Access"
UNAUTHORIZED_THREAT_ACCESS = "Unauthorized Threat Access"


class Authenticator:
    @staticmethod
    def role_access_check(requestPath):
        leadingPath = requestPath.split("/")[1]
        if current_user.role_id in PATH_ROLE_LIST[leadingPath]:
            return True
        flash(UNAUTHORIZED_ROUTE_ACCESS)
        return False

    # validate threat_id is exist first
    # if user is citizen, validate if the citizen is the reporter of the threat first
    # since a citizen can only access and comment on the threat related to herself/himself
    @staticmethod
    def citizen_access_check(threat_id):
        if current_user.role_id == 1:
            if not current_user.id == Threat.query.filter_by(id=threat_id).first().user_id:
                flash(UNAUTHORIZED_THREAT_ACCESS)
                return False
            return True
        return False
