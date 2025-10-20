from sqlalchemy import Column, String, Integer, Float
from .base import Base

from .User import USER_NAME_LEN

from begin.globals import Token

import time

##
IP_LEN = 16

#
class IpInfos(Base):
    __tablename__ = 'IpInfos'

    ip = Column(String(IP_LEN), primary_key=True)

    user_name = Column(String(USER_NAME_LEN))

    email_send_count = Column(Integer)
    email_send_last_time = Column(Float)

    auth_attempts = Column(Integer)

    block_time_init = Column(Float)

    validity = Column(Float)

    ##
    def __init__(self, ip:str=None \
            ,user_name:str=None \
            ,email_send_count:int=0, email_send_last_time:int=0, auth_attempts:int = 0 \
            ,block_time_init:float|None= None \
            ,validity = time.time() + Token.VALIDITY_IPINFOS)->None:

        self.ip = ip
        self.user_name = user_name

        self.email_send_count = email_send_count
        self.email_send_last_time = email_send_last_time
        self.auth_attempts = auth_attempts

        self.block_time_init = block_time_init
        
        self.validity = validity


    @property 
    def email_send_status(self)->int:
        from begin.globals import Email, Token
        from database import session

        import time

        ##
        if self.block_time_init != None and self.block_time_init + Token.VALIDITY_IPINFOS_BLOCK<= time.time():
            self.block_time_init = None

            self.email_send_count = 0
            self.auth_attempts = 0


            session.commit()

        elif self.block_time_init != None:
            return Email.SEND_NOT_ALLOW_BECAUSE_IP_BLOCKED

        #
        if self.email_send_last_time + Email.SEND_INTERVAL > time.time():
            return Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL

        if self.email_send_count >= Email.SEND_MAX:
            self.block_time_init = time.time()
            session.commit()

            return Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT

        if self.auth_attempts >= Token.AUTH_ATTEMPTS_MAX:
            self.block_time_init = time.time()
            session.commit()

            return Email.SEND_NOT_ALLOW_BECAUSE_TOKEN_ATTEMPTS

        return Email.SEND_OK

    @property
    def email_send_time_allow(self)->float:
        from begin.globals import Email
        import time

        ##
        send_status = self.email_send_status
        print(self.email_send_count, Email.SEND_MAX)

        if send_status == Email.SEND_OK:
            return time.time()

        #
        if self.block_time_init != None:
            return self.block_time_init + Token.VALIDITY_IPINFOS_BLOCK

        if send_status == Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL:
            return self.email_send_last_time + Email.SEND_INTERVAL


    @property
    def client_behavior_normal(self)->bool:
        from begin.globals import Email, Token

        ##
        if self.email_send_count >= Email.SEND_MAX:
            return False

        if self.auth_attempts >= Token.AUTH_ATTEMPTS_MAX:
            return False 

        if self.block_time_init != None:
            return False

        return True


    def status_update(self)->None:
        self.email_send_status
