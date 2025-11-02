from database.session import Base

#
class IpInfos(Base):
    __tablename__ = 'IpInfos'

    AUTH_ATTEMPTS_MAX = 30

    VALIDITY = 60*60*24*7
    VALIDITY_BLOCK = 60*20

    ##
    def __init__(self, **kwargs)->None:
        from database import model_update
        import time

        ##
        model = type("model", (self.__class__, ), {})
        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])

        self.validity = time.time() + self.VALIDITY


    @property 
    def email_send_status(self)->int:
        from begin.globals import Email, Auth
        from database import session, model_update

        import time

        ##
        if self.block_time_init != None and self.block_time_init + self.VALIDITY_BLOCK<= time.time():
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

        if self.auth_attempts >= self.AUTH_ATTEMPTS_MAX:
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
            return self.block_time_init + self.VALIDITY_BLOCK

        if send_status == Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL:
            return self.email_send_last_time + Email.SEND_INTERVAL


    @property
    def client_behavior_normal(self)->bool:
        from begin.globals import Email

        ##
        if self.email_send_count >= Email.SEND_MAX:
            return False

        if self.auth_attempts >= self.AUTH_ATTEMPTS_MAX:
            return False 

        if self.block_time_init != None:
            return False

        return True


    def status_update(self)->None:
        self.email_send_status
