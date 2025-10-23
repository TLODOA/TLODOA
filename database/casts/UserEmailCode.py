from sqlalchemy import Column, ForeignKey, String, Float, Integer
from begin.globals import Token, Email

from .base import Base

from .IpInfos import IP_LEN
from .User import USER_NAME_LEN, USER_EMAIL_LEN

##
class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    ip = Column(String(IP_LEN), ForeignKey('IpInfos.ip'))

    name = Column(String(USER_NAME_LEN), ForeignKey('User.name'))
    email = Column(String(USER_EMAIL_LEN))

    token = Column(String(Token.HASH_EMAIL_TOKEN_LEN), primary_key=True)
    validity = Column(Float)

    field = Column(Integer)

    ##
    def __init__(self \
            ,ip:str=None \
            ,name:str=None, email:str=None \
            ,token:str=None, validity=None \
            ,field:str=Email.FIELD_UNDEFINED)->None:

        from begin.globals import Token
        import time

        ##
        if token == None:
            token = Token.email_generate()

        if validity == None:
            validity = time.time() + Email.VALIDITY

        #
        self.ip = ip

        self.name = name
        self.email = email

        self.token = token
        self.validity = validity

        self.field = field

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

        self.token = Token.crypt_hash(self.token, hash_len=Token.HASH_EMAIL_TOKEN_LEN)

        session.commit()

    def token_auth(self, token_input)->bool:
        from database import session, session_get, IpInfos
        from begin.globals import Token

        ##
        ipInfos = session_get(IpInfos, ip=self.ip)[0]
        ipInfos.auth_attempts += 1

        session.commit()

        #
        return Token.crypt_hash_auth(self.token, token_input)

    def token_valid(self)->bool:
        import time

        if self.validity < time.time():
            return False

        return True
