from sqlalchemy import Column, String, Integer, Float, CHAR
from begin.globals import Token

from .base import Base
from .User import USER_NAME_LEN

from .crypt import *

import time

##
IP_LEN = 16

#
class IpInfos(Base):
    __tablename__ = 'IpInfos'

    FIELD_CIPHER= [ "cipher_ip" ]
    FIELD_HASHED = [ "hashed_ip" ]

    ##
    dek = Column(CHAR(Token.DEK_LEN))

    cipher_ip = Column(String())

    #
    email_send_count = Column(Integer)
    email_send_last_time = Column(Float)
    auth_attempts = Column(Integer)

    block_time_init = Column(Float)
    validity = Column(Float)

    #
    hashed_ip = Column(String(Token.FIELD_HASHED_SIZE), primary_key=True, index=True)

    ##
    def __init__(self \
            ,ip:str=None \
            ,email_send_count:int=0, email_send_last_time:int=0, auth_attempts:int = 0 \
            ,block_time_init:float|None= None \
            ,validity = time.time() + Token.VALIDITY_IPINFOS)->None:
        
        from database import model_update

        ##
        dek = AESGCM.generate_key(bit_length=256)
        self.dek = key_wrap(dek)

        model_update(self \
                ,cipher_ip=ip, hashed_ip=ip \
                ,email_send_count=email_send_count, email_send_last_time=email_send_last_time \
                ,auth_attempts=auth_attempts \
                ,block_time_init=block_time_init \
                ,validity=validity)

    @property 
    def email_send_status(self)->int:
        from begin.globals import Email, Token
        from database import session, model_update

        import time

        ##
        if self.block_time_init != None and self.block_time_init + Token.VALIDITY_IPINFOS_BLOCK<= time.time():
            model_update(self \
                    ,block_time_init=None \
                    ,email_send_count=0, auth_attempts=0)

        elif self.block_time_init != None:
            return Email.SEND_NOT_ALLOW_BECAUSE_IP_BLOCKED

        #
        if self.email_send_last_time + Email.SEND_INTERVAL > time.time():
            return Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL

        if self.email_send_count >= Email.SEND_MAX:
            model_update(self, block_time_init=time.time())

            return Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT

        if self.auth_attempts >= Token.AUTH_ATTEMPTS_MAX:
            model_update(self, block_time_init=time.time())

            return Email.SEND_NOT_ALLOW_BECAUSE_TOKEN_ATTEMPTS

        return Email.SEND_OK

    @property
    def email_send_time_allow(self)->float:
        from begin.globals import Email
        import time

        ##
        send_status = self.email_send_status

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
