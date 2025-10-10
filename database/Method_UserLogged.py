from .session import session
from .casts import *

from begin import error_message

##
def userLogged_insert(user_name:str, ip:str)->None:
    try:
        userLogged = UserLogged(user_name=user_name, ip=ip)
        session.add(userLogged)
    except Exception as e:
        session.rollback()
        error_message('userLogged_insert', e)

        return

    session.commit()


##
def userLogged_get(user_name:str=None, ip:str=None)->tuple|None:
    try:
        userLogs = None
        filters = []

        if user_name:
            filters.append(UserLogged.name == user_name)

        if ip:
            filters.append(UserLogged.ip == ip)

        userLogs = session.query(UserLogged).filter(*filters).all()
        return userLogs

    except Exception as e:
        session.rollback()
        error_message('userLogged_get', e)

        return
