from sqlalchemy import Column, String, Integer, Float, ForeignKey, CHAR
from begin.globals import Token

from .base import Base
from .IpInfos import IP_LEN
from .User import USER_NAME_LEN

from .crypt import *

import time

##

class UserToken(Base):
    __tablename__ = 'UserToken'

    FIELD_CIPHER = ["cipher_ip", "cipher_userName", "cipher_token"]
    FIELD_HASHED = ["hashed_ip", "hashed_userName", "hashed_token"]

    ##
    dek = Column(CHAR(Token.DEK_LEN))

    cipher_ip = Column(String())
    cipher_token = Column(String(), primary_key=True)
    cipher_userName = Column(String())

    validity = Column(Float)

    #
    hashed_ip = Column(CHAR(Token.FIELD_HASHED_SIZE), index=True)
    hashed_userName = Column(CHAR(Token.FIELD_HASHED_SIZE), index=True)

    ##
    def __init__(self \
            ,ip:str=None \
            ,token:str=None \
            ,user_name:str=None \
            ,validity:str=time.time() + Token.VALIDITY_KEY_USER )->None:

        from database import model_update
        from begin.globals import Token

        ##
        if token == None:
            token = Token.user_generate()

        dek = AESGCM.generate_key(bit_length=256)
        token_hashed =  Token.crypt_phash(token, hash_len=Token.PHASH_USER_TOKEN_LEN)

        self.dek = key_wrap(dek)

        model_update(self \
                ,cipher_ip=ip, hashed_ip=ip \
                ,cipher_userName=user_name, hashed_userName=user_name \
                ,cipher_token=token_hashed \
                ,validity=validity)

    def token_auth(self, token_input:str)->bool:
        from database import model_get
        from begin.globals import Token

        ##
        token = model_get(self, "cipher_token")[0]

        return Token.crypt_phash_auth(token, token_input)
