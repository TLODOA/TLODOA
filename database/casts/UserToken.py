from sqlalchemy import Column, String, Integer, Float, ForeignKey
from .base import Base

from .IpInfos import IP_LEN
from .User import USER_NAME_LEN

from begin.globals import Token

import time

##

class UserToken(Base):
    __tablename__ = 'UserToken'

    token = Column(String(Token.KEY_USER_LEN), primary_key=True)
    ip = Column(String(IP_LEN), ForeignKey('IpInfos.ip'))

    user_name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))

    validity = Column(Float)

    ##
    def __init__(self, token:str=None \
            ,ip:str=None \
            ,user_name:str=None \
            ,validity:str=time.time() + Token.VALIDITY_KEY_USER )->None:

        if token == None:
            token = Token.user_generate()

        self.token = token
        self.ip = ip

        self.user_name = user_name

        self.validity = validity


    def token_auth(token_input:str)->bool:
        from database import session_get, session_update, ipInfos

        ipInfos = session_get(IpInfos, ip=ip)

        if token_input == self.token:
            return True

        session_update(ipInfos, "auth_attempts", ipInfos[0] + 1)

        return False
