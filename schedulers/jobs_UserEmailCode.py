from begin.xtensions import *
from begin.error_handler import error_message

from database import *

##
def userEmailCode_invalid_get()->tuple|None:
    try:
        userEmail = session.query(UserEmailCode) \
                .filter(UserEmailCode.validity < time.time()) \
                .all()

        return userEmail

    except Exception as e:
        error_message('userEmailCode_invalid_get', e)

        return None

def userEmailCode_invalid_delete()->None:
    try:
        userEmail_invalid = userEmailCode_invalid_get()
        session_delete(userEmail_valid)

    except Exception as e:
        error_message('userEmailCode_invalid_remove', e)

#
def jobs()->tuple:
    from begin.globals.Scheduler import Task

    ##
    jobs = (
            Task(userEmailCode_invalid_delete),
        )

    return jobs
