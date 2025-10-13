from .session import session
from .casts import *

from begin import error_message

import time

##
UserEmailCode_VALIDITY = 60*10 # half hour

def userEmailCode_insert(user_name:str, email:str,\
        ip:str, token:str, validity:float=time.time()+UserEmailCode_VALIDITY)->object:
    try:
        userEmailCode = UserEmailCode(name=user_name, email=email, ip=ip, token=token, validity=validity)
        session.add(userEmailCode)
    except Exception as e:
        error_message('userEmailCode_insert', e)
        session.rollback()

        return

    session.commit()

    return userEmailCode

def userEmailCode_delete(userEmailCode:tuple)->None:
    try:
        session.delete(*userEmailCode)
    except Exception as e:
        session.rollback()
        error_message('userEmailCode_delete', e)

        return

    session.commit()

#
def userEmailCode_get(user_name:str=None, ip:str=None, email:str=None)->tuple|None:
    try:
        userEmailCode = ()
        filters = []

        if user_name:
            filters.append(UserEmailCode.name == user_name)
        if email:
            filters.append(UserEmailCode.email == email)
        if ip:
            filters.append(UserEmailCode.ip == ip)

        userEmailCode = session.query(UserEmailCode).filter(*filters).all()

        return userEmailCode

    except Exception as e:
        session.rollback()
        error_message('userEmailCode_get', e)

        return None
