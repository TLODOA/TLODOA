from sqlalchemy import Column, String, Integer
from .base import Base

from begin.globals import Token

##
USER_NAME_LEN = 100
USER_EMAIL_LEN = 240
USER_PASSWORD_LEN = 50

##
class User(Base):
    __tablename__ = 'User'

    name = Column(String(USER_NAME_LEN), primary_key=True)
    email = Column(String(USER_EMAIL_LEN))
    password = Column(String(Token.HASH_USER_PASSWORD_LEN))

    status = Column(Integer)

    ##
    def __init__(self, name:str=None, email:str=None, password:str=None, status:str=None)->None:
        from begin.globals import Token

        self.name = name
        self.email = email
        self.password = Token.crypt_hash(password, hash_len=USER_PASSWORD_LEN)

        self.status = status

    def password_auth(self, password_input)->bool:
        from begin.globals import Token

        ##
        return Token.crypt_hash_auth(self.password, password_input)
