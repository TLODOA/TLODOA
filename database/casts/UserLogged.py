from sqlalchemy import Column, String, ForeignKey
from .base import Base

from .User import USER_NAME_LEN

IP_LEN = 19

##
class UserLogged(Base):
    __tablename__ = 'UserLogged'

    name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))
    ip = Column(String(IP_LEN), primary_key=True)
