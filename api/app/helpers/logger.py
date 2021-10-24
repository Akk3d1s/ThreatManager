from flask import flash
from app.models.action_log import ActionLog
from app.models.error_log import ErrorLog

class Logger:
    @staticmethod
    def success(route, action, user_id):
        action_log = ActionLog(route=route, action=action, user_id=user_id)
        action_log.save()

    @staticmethod
    def fail(route, error, user_id):
        error_log = ErrorLog(route=route, error=error, user_id=user_id)
        error_log.save()