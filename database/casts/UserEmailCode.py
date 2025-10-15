from sqlalchemy import Column, ForeignKey, String, Float
from begin.globals import Token

from .base import Base

from .IpInfos import IP_LEN
from .User import USER_NAME_LEN, USER_EMAIL_LEN

import time

##
UserEmailCode_VALIDITY = 60*10 # half hour

class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    ip = Column(String(IP_LEN), ForeignKey('IpInfos.ip'), primary_key=True)

    name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))
    email = Column(String(USER_EMAIL_LEN))

    token = Column(String(Token.KEY_EMAIL_LEN))
    validity = Column(Float)

    ##
    def __init__(self, ip:str=None \
            ,name:str=None, email:str=None \
            ,token=None, validity=time.time()+UserEmailCode_VALIDITY)->None:

        self.ip = ip

        self.name = name
        self.email = email

        self.token = token
        self.validity = validity

    def token_send(self)->None:
        import smtplib
        from email.message import EmailMessage

        from begin.globals import Email, SMTP
        from database import session, session_get, IpInfos

        import time

        ##
        ipInfos = session_get(IpInfos, ip=self.ip)[0]
        status = ipInfos.email_send_status

        print('status send: ', status)
        if status != Email.SEND_OK:
            return

        ##
        msg = EmailMessage()
        msg['Subject'] = 'TLODOA email token'
        msg['From'] = SMTP.SENDER
        msg['To'] = self.email

        msg.set_content(f'This is your email token: {self.token}')

        # This code passage doesn't works in the shit computers of school
        """
        with smtplib.SMTP(SMTP.SERVER, SMTP.PORT) as server:
            server.starttls()
            server.login(SMTP.SENDER, SMTP.APP_PASSWORD)
            server.send_message(msg)
            """

        ##
        ipInfos.email_send_last_time = time.time()
        ipInfos.email_send_count += 1

        session.commit()

    def token_auth(self, token_input)->bool:
        from database import session, session_get, IpInfos

        if self.token == token_input:
            return True

        ipInfos = session_get(IpInfos, ip=self.ip)[0]
        ipInfos.auth_attempts += 1

        session.commit()

        return False
