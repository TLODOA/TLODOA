from begin.globals import Scheduler

from database import *
from begin.error_handler import error_message

##
def ipInfos_invalid_get()->tuple|None:
    import time

    try:
        ipInfos = session.query(IpInfos) \
                .filter(IpInfos.validity <= time.time()) \
                .all()

        return ipInfos

    except Exception as e:
        error_message('IpInfos_invalid_get', e)
        session.rollback()

def ipInfos_invalid_delete()->None:
    try:
        ipInfos = ipInfos_invalid_get()

        if not len(ipInfos):
            return

        session_delete(ipInfos)

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
