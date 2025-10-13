from sqlalchemy import Column, ForeignKey, String, Float
from begin.globals import Token

from .base import Base

from .IpInfos import IP_LEN
from .User import USER_NAME_LEN, USER_EMAIL_LEN

##
class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    ip = Column(String(IP_LEN), ForeignKey('IpInfos.ip'), primary_key=True)

    name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))
    email = Column(String(USER_EMAIL_LEN))

    token = Column(String(Token.KEY_EMAIL_LEN))
    validity = Column(Float)

    ##
    def token_send(self)->None:
        import smtplib
        from email.message import EmailMessage

        from begin.globals import Email, SMTP
        from database import session, ipInfos_get

        import time

        ##
        ipInfos = ipInfos_get(ip=self.ip)[0]
        status = ipInfos.email_send_status()

        if status != Email.SEND_OK:
            return

        ##
        msg = EmailMessage()
        msg['Subject'] = 'TLODOA email token'
        msg['From'] = SMTP.SENDER
        msg['To'] = self.email

        msg.set_content(f'This is your email token: {self.token}')

        #
        with smtplib.SMTP(SMTP.SERVER, SMTP.PORT) as server:
            server.starttls()
            server.login(SMTP.SENDER, SMTP.APP_PASSWORD)
            # server.send_message(msg)

        ##
        ipInfos.email_send_last = time.time()
        ipInfos.email_count += 1

        session.commit()

    def token_auth(self, token_input)->bool:
        from databse import session, ipInfos_get

        if self.token == token_input:
            return True

        ipInfos = ipInfos_get(ip=self.ip)[0]

        ipInfos.email_token_attemps += 1

        session.commit()
