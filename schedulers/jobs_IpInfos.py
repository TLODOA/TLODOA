from begin.globals import Scheduler

from database import *
from begin.error_handler import error_message

##
def IpInfos_invalid_get()->tuple|None:
    import time

    try:
        ipInfos = session.query(IpInfos) \
                .filter(IpInfos.validity <= time.time()) \
                .all()

        return ipInfos

    except Exception as e:
        error_message('IpInfos_invalid_get', e)
        session.rollback()

def IpInfos_invalid_delete()->None:
    try:
        ipInfos = IpInfos_invalid_get()

        if not len(ipInfos):
            return

        session_delete(ipInfos)

    except Exception as e:
        error_message('IpInfos_invalid_delete', e)

##
def jobs(scheduler:object)->None:
    scheduler.add_job(func=IpInfos_invalid_delete, trigger=Scheduler.TRIGGER, seconds=60*24)
