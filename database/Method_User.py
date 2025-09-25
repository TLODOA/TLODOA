from .session import session
from .casts import *

from begin import error_message

##
def user_get(user_name: str)->object:
    user = None
    try:
        user = session.query(User.name, User.email, User.password).filter(User.name == user_name).first()
    except Exception as e:
        error_message('user_get', e)
        session.rollback()

        return None

    return user

def user_insert(user_name, user_email, user_password)->None:
    try:
        user = User(name=user_name, email=user_email, password=user_password)
        session.add(user)
    except Exception as e:
        error_message('user_insert', e)
        return

    session.commit()
