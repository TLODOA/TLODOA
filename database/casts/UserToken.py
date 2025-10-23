from sqlalchemy import Column, String, Integer, Float, ForeignKey
from .base import Base

from .IpInfos import IP_LEN
from .User import USER_NAME_LEN

from begin.globals import Token

import time

##

class UserToken(Base):
    __tablename__ = 'UserToken'

    token = Column(String(Token.HASH_USER_TOKEN_LEN), primary_key=True)
    ip = Column(String(IP_LEN), ForeignKey('IpInfos.ip'))

    user_name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))

    validity = Column(Float)

    ##
    def __init__(self, token:str=None \
            ,ip:str=None \
            ,user_name:str=None \
            ,validity:str=time.time() + Token.VALIDITY_KEY_USER )->None:

        from begin.globals import Token

        ##
        if token == None:
            token = Token.user_generate()

        self.token = Token.crypt_hash(token, hash_len=Token.KEY_USER_LEN)
        self.ip = ip

        self.user_name = user_name

        self.validity = validity


    def token_auth(self, token_input:str)->bool:
        from database import session_get, session_update, IpInfos
        from begin.globals import Token

        ##
        return Token.crypt_hash_auth(self.token, token_input)
