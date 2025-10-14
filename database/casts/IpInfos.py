from sqlalchemy import Column, String, Integer, Float
from .base import Base

from .User import USER_NAME_LEN

import time

##
IP_LEN = 16

#
IpInfos_VALIDITY = 60*60*24*7 # one week

class IpInfos(Base):
    __tablename__ = 'IpInfos'

    ip = Column(String(IP_LEN), primary_key=True)

    user_name = Column(String(USER_NAME_LEN))

    email_count = Column(Integer)
    email_send_last = Column(Float)
    email_token_attempts = Column(Integer)

    validity = Column(Float)

    ##
    def __init__(self, ip:str=None\
            ,user_name:str=None \
            ,email_count:int=0, email_send_last:int=0, email_token_attempts:int = 0 \
            ,validity = time.time() + IpInfos_VALIDITY)->None:

        self.ip = ip
        self.user_name = user_name

        self.email_count = email_count
        self.email_send_last = email_send_last
        self.email_token_attempts = email_token_attempts
        
        self.validity = validity


    def email_send_status(self)->int:
        from begin.globals import Email
        import time

        ##
        if self.email_send_last + Email.SEND_INTERVAL > time.time():
            return Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL

        if self.email_count >= Email.SEND_MAX:
            return Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT

        return Email.SEND_OK
