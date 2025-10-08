from sqlalchemy import Column, ForeignKey, String
from .base import Base

from .User import USER_NAME_LEN

IP_LEN = 19
TOKEN_LEN = 7

class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))
    ip = Column(String(IP_LEN), primary_key=True)

    token = Column(String(TOKEN_LEN))

    ##
    def token_add(token:str)->None:
        self.token = token

    def token_comp(token:str) -> bool:
        return token == self.token
