from database import *
from begin.error_handler import error_message

##
def userToken_invalid_delete()->None:
    try:
        userToken_invalid = session_get(UserToken, validity__lt=time.time())

        session_delete(userToken_invalid)
    except Exception as e:
        error_message('userToken_invalid_delete', e)

#
def jobs()->tuple:
    from begin.globals.Scheduler import Task

    jobs = (
            Task(func=userToken_invalid_delete, seconds=60*60*12),
        )

    return jobs
