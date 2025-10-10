from .session import session
from .casts import *

from begin import error_message

##
def userEmailCode_insert(user_name:str, email:str, ip:str, token:str)->object:
    try:
        userEmailCode = UserEmailCode(name=user_name, email=email, ip=ip, token=token)
        session.add(userEmailCode)
    except Exception as e:
        error_message('userEmailCode_insert', e)
        session.rollback()

        return

    session.commit()

    return userEmailCode


def userEmailCode_get(user_name:str=None, ip:str=None, email:str=None)->tuple|None:
    try:
        userEmailCode = None
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
