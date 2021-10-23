from flask import flash
from flask_login import current_user
from app import app, db
from app.models.log import ActionLog, ErrorLog

PATH_ACTION_LIST = {
    'api_credential': "inspected credential",
    'newcase_application': "Applied for New Case",
    'newcase_approve': "Approved New Case",
    'newcase_reject': "Rejected New Case",
    'endcase_application': "Applied for End Case",
    'endcase_approve': "Approved End Case",
    'endcase_reject': "Rejected End Case",
    'role_application': "Applied Role Change",
    'role_application_list': "View Role Application List",
    'role_application_approve': "Approved Role Change Application",
    'role_application_reject': "Rejected Role Change Application",
    'comment': "Comment Sent",
    'download_file_threat': "Downloaded Threat Attachment Files",
    'download_file_comment': "Downloaded Comment Attachment Files",
    'download_all_cases_csv': "Downloaded Threats as CSV",
    'report': "Reported New Threat"
}

class Logger:
    @staticmethod
    def success(requestPath):
        leadingPath = requestPath.split("/")[1]
        actionLog = ActionLog(route=requestPath, action=PATH_ACTION_LIST[leadingPath], user_id=current_user.id)
        db.session.add(actionLog)
        db.session.commit()
        flash(PATH_ACTION_LIST[leadingPath])

    @staticmethod
    def fail(requestPath, error):
        leadingPath = requestPath.split("/")[1]
        errorLog = ErrorLog(route=requestPath, error=str(error), user_id=current_user.id)
        db.session.add(errorLog)
        db.session.commit()
        flash(PATH_ACTION_LIST[leadingPath]+" Failed")