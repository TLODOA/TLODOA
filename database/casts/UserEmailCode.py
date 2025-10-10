from sqlalchemy import Column, ForeignKey, String
from .base import Base

from .User import USER_NAME_LEN, USER_EMAIL_LEN
from .UserLogged import IP_LEN

from begin.globals import SMTP_SENDER, SMTP_APP_PASSWORD, SMTP_SERVER, SMTP_PORT

TOKEN_LEN = 7

class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))
    email = Column(String(USER_EMAIL_LEN))

    ip = Column(String(IP_LEN), primary_key=True)
    token = Column(String(TOKEN_LEN))

    ##
    def token_send(self)->None:
        import smtplib
        from email.message import EmailMessage

        ##
        msg = EmailMessage()
        msg['Subject'] = 'TLODOA email token'
        msg['From'] = SMTP_SENDER
        msg['To'] = self.email

        msg.set_content(f'This is your email token: {self.token}')

        #
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_SENDER, SMTP_APP_PASSWORD)
            server.send_message(msg)
