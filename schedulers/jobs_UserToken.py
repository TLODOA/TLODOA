from database import *
from begin.error_handler import error_message

##
def userToken_invalid_get()->tuple|None:
    try:
        userToken_invalid = session.query(UserToken) \
                .filter(UserToken.validity < time.time()) \
                .all()

        return userToken

    except Exception as e:
        error_message('userToken_invalid_get', e)

        return None

def userToken_invalid_delete()->None:
    try:
        userToken_invalid = userToken_invalid_get()

        session_delete(userToken)
    except Exception as e:
        error_message('userToken_invalid_delete', e)

#
def jobs()->tuple:
    from begin.globals.Scheduler import Task

    jobs = (
            Task(func=userToken_invalid_delete, seconds=60*60*12),
        )

    return jobs
