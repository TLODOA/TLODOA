from begin.globals import Messages
from begin.xtensions import *

from database import *

##
def userEmailCode_invalid_delete()->None:
    try:
        userEmail_invalid = session_get(UserEmailCode, validity__lt=time.time())
        session_delete(userEmail_invalid)

    except Exception as e:
        Messages.error('userEmailCode_invalid_remove', e)

#
def jobs()->tuple:
    from begin.globals.Scheduler import Task

    ##
    jobs = (
            Task(userEmailCode_invalid_delete),
        )

    return jobs
