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
    hashed_ip = Column(CHAR(32), index=True)
    hashed_userName = Column(CHAR(32), index=True)

    ##
    def __init__(self \
            ,ip:str=None \
            ,token:str=None \
            ,user_name:str=None \
            ,validity:str=time.time() + Token.VALIDITY_KEY_USER )->None:

        from begin.globals import Token

        ##
        if token == None:
            token = Token.user_generate()

        dek = AESGCM.generate_key(bit_length=256)
        token_hashed =  Token.crypt_hash(token, hash_len=Token.KEY_USER_LEN)

        self.dek = key_wrap(dek)

        self.cipher_ip = field_encrypt(dek, ip)
        self.cipher_token = field_encrypt(dek, token_hashed)
        self.cipher_userName = field_encrypt(dek, user_name)

        self.validity = validity

        #
        self.hashed_ip = Token.crypt_hash256(ip)
        self.hashed_userName = Token.crypt_hash256(user_name)


    def token_auth(self, token_input:str)->bool:
        from database import model_get
        from begin.globals import Token

        ##
        token = model_get(self, "cipher_token")[0]

        return Token.crypt_hash_auth(token, token_input)
