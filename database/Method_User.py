from .session import session
from .casts import *

from begin import error_message

##
def user_insert(name:str=None, email:str=None, password:str=None)->None:
    try:
        user = User(name=name, email=email, password=password)
        session.add(user)
    except Exception as e:
        error_message('user_insert', e)
        return

    session.commit()

def user_get(name: str=None, email:str=None, password:str=None)->tuple|None:
    try:
        user = ()
        filters = []

        if name:
            filters.append(User.name == name)
        if email:
            filters.append(User.email == email)
        if password:
            filters.append(User.password = password)

        user = session.query(User).filter(*filters)

        return user

    except Exception as e:
        session.rollback()
        error_message('user_get', e)

        return None
