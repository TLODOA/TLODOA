from .session import session
from .casts import *

from begin import error_message

##
def userEmailCode_insert(user_name:str, ip:str)->None:
    try:
        userEmailCode = UserEmailCode(name = user_name, ip=ip, token=None)
        session.add(userEmailCode)
    except Exception as e:
        error_message('userEmailCode_insert', e)
        session.rollbakc()

        return

    session.commit()
