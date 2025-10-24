from begin.error_handler import error_message
from database import *

##
def ipInfos_invalid_delete()->None:
    try:
        ipInfos_invalid = session_get(IpInfos, validity__lt=time.time())

        if not len(ipInfos_invalid):
            return

        session_delete(ipInfos_invalid)

    except Exception as e:
        error_message('IpInfos_invalid_delete', e)

##
def jobs()->tuple:
    from begin.globals.Scheduler import Task

    ##
    jobs = (
            Task(ipInfos_invalid_delete),
        )

    return jobs
