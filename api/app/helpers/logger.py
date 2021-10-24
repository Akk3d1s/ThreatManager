'''Logger file'''
from app.models.action_log import ActionLog
from app.models.error_log import ErrorLog

class Logger:
    '''Logger in order to track actions accross the API'''
    @staticmethod
    def success(route, action, user_id):
        '''Record success actions'''
        action_log = ActionLog(route=route, action=action, user_id=user_id)
        action_log.save()

    @staticmethod
    def fail(route, error, user_id):
        '''Record failed actions'''
        error_log = ErrorLog(route=route, error=error, user_id=user_id)
        error_log.save()
