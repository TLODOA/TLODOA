from sqlalchemy import Column, String, Integer, CHAR
from begin.globals import Token

from .base import Base
from .crypt import *

##
USER_NAME_LEN = 100
USER_EMAIL_LEN = 240
USER_PASSWORD_LEN = 50

##
class User(Base):
    __tablename__ = 'User'

    FIELD_CIPHER = ["cipher_name", "cipher_email", "cipher_password"]
    FIELD_HASHED = ["hashed_name", "hashed_email"]

    ##
    dek = Column(CHAR(Token.DEK_LEN))

    cipher_name = Column(String())
    cipher_email = Column(String())
    cipher_password = Column(String())

    status = Column(Integer)

    #
    hashed_name = Column(String(32), primary_key=True, index=True)
    hashed_email = Column(String(32), index=True)

    ##
    def __init__(self, name:str=None, email:str=None, password:str=None, status:str=None)->None:

        from database import model_update
        from begin.globals import Token

        ##
        dek = AESGCM.generate_key(bit_length=256)
        self.dek = key_wrap(dek)

        password_hashed = Token.crypt_hash(password, hash_len=Token.HASH_USER_PASSWORD_LEN)

        model_update(self \
                ,cipher_name=name, hashed_name=name \
                ,cipher_email=email, hashed_email=email \
                ,cipher_password=password_hashed \
                ,status=status)

    def password_auth(self, password_input:str)->bool:
        from begin.globals import Token
        from database.session import model_get

        ##
        password = model_get(self, "cipher_password")[0]
        print('password_hashed: ', password)

        return Token.crypt_hash_auth(password, password_input)
