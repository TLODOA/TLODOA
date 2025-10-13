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
    email_token_attempts = Column(Integer)

    validity = Column(Float)

    ##
    def email_send_status(self)->int:
        from begin.globals import Email
        import time

        ##
        if self.email_send_last + Email.SEND_INTERVAL > time.time():
            return Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL

        if self.email_count >= Email.SEND_MAX:
            return Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT

        return Email.SEND_OK
