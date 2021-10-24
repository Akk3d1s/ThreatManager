from flask import flash
from flask_login import current_user

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

class Authenticator:
    @staticmethod
    def route_access_check(request_path):
        leading_path = request_path.split("/")[1]
        if current_user.role_id in PATH_ROLE_LIST[leading_path]:
            return True
        flash('Unauthorized Access')
        return False
