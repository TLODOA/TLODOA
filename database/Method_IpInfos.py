from .session import session
from .casts import *

from begin.error_handler import error_message

import sqlalchemy
import time

##
IpInfos_VALIDITY = 60*60*24*7 # one week

def ipInfos_insert(ip:str=None, \
        user_name:str=None, email_count:int=0, email_send_last:float=0, \
        validity:float=(time.time()+IpInfos_VALIDITY))->None|object:
    try:
        ipInfos = IpInfos(ip=ip, user_name=user_name, email_count=email_count, email_send_last=0, validity=validity)

        session.add(ipInfos)
    except Exception as e:
        session.rollback()
        error_message('ipInfos_insert', e)

        return None

    session.commit()
    return ipInfos

def ipInfos_delete(ipInfos:tuple)->None:
    try:
        session.delete(*ipInfos)
    except Exception as e:
        session.rollback()
        error_message('ipInfos_delete', e)

        return

    session.commit()

#
def ipInfos_get(ip:str=None, user_name:str=None, email_count:int=None, email_send_last:float=None)->tuple|None:
    try:
        ipInfos = None
        filters = []

        if ip:
            filters.append(IpInfos.ip == ip)
        if user_name:
            filters.append(IpInfos.user_name == user_name)
        if email_count != None:
            filters.append(IpInfos.email_count == email_count)
        if email_send_last != None:
            filters.append(IpInfos.email_send_last == email_send_last)

        ipInfos = session.query(IpInfos).filter(*filters).all()
        return ipInfos

    except Exception as e:
        session.rollback()
        error_message('ipInfos_get', e)

        return None
