from sqlalchemy import Column, String, Integer, Float
from .base import Base

from .User import USER_NAME_LEN

##
IP_LEN = 16

class IpInfos(Base):
    __tablename__ = 'IpInfos'

    ip = Column(String(IP_LEN), primary_key=True)

    user_name = Column(String(USER_NAME_LEN))
    email_count = Column(Integer)
    email_send_last = Column(Float)

    validity = Column(Float)
