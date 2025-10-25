from sqlalchemy import Column, ForeignKey, String, Float, Integer, CHAR
from begin.globals import Token, Email

from .base import Base
from .IpInfos import IP_LEN
from .User import USER_NAME_LEN, USER_EMAIL_LEN

from .crypt import *

##
class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    FIELD_CIPHER = ["cipher_ip", "cipher_name", "cipher_email", "cipher_token"]
    FIELD_HASHED = ["hashed_ip", "hashed_name", "hashed_email"]
    
    ##
    dek = Column(CHAR(Token.DEK_LEN))

    cipher_ip = Column(String())
    cipher_name = Column(String())
    cipher_email = Column(String())
    cipher_token = Column(String(), primary_key=True)

    validity = Column(Float)

    field = Column(Integer)

    #
    hashed_ip = Column(CHAR(32), ForeignKey("IpInfos.hashed_ip"), index=True)
    hashed_name = Column(CHAR(32), index=True)
    hashed_email = Column(CHAR(32), index=True)

    ##
    def __init__(self \
            ,ip:str=None \
            ,name:str=None, email:str=None \
            ,token:str=None, validity=None \
            ,field:str=Email.FIELD_UNDEFINED)->None:

        from begin.globals import Token
        import time

        ##
        if token is None:
            token = Token.email_generate()

        if validity is None:
            validity = time.time() + Email.VALIDITY

        #
        dek = AESGCM.generate_key(bit_length=256)
        self.dek = key_wrap(dek)

        self.cipher_ip = field_encrypt(dek, ip)
        self.cipher_name = field_encrypt(dek, name)
        self.cipher_email = field_encrypt(dek, email)
        self.cipher_token = field_encrypt(dek, token)

        self.validity = validity

        self.field = field

        #
        self.hashed_ip = Token.crypt_hash256(ip)
        self.hashed_name = Token.crypt_hash256(name)
        self.hashed_email = Token.crypt_hash256(email)

    def token_send(self)->None:
        from email.message import EmailMessage
        import smtplib

        from database import session, session_update, session_get, model_get, model_update, IpInfos
        from begin.globals import Email, SMTP

        import time

        ##
        ipInfos = session_get(IpInfos, hashed_ip=self.hashed_ip)
        status = ipInfos[0].email_send_status

        print('status send: ', status)
        if status != Email.SEND_OK:
            return

        ##
        email = model_get(self, "cipher_email")[0]
        token = model_get(self, "cipher_token")[0]

        #
        msg = EmailMessage()
        msg['Subject'] = 'TLODOA email token'
        msg['From'] = SMTP.SENDER
        msg['To'] = email

        msg.set_content(f'This is your email token: {token}')

        # This code passage doesn't works in the shit computers of school
        """
        with smtplib.SMTP(SMTP.SERVER, SMTP.PORT) as server:
            server.starttls()
            server.login(SMTP.SENDER, SMTP.APP_PASSWORD)
            server.send_message(msg)
            """

        ##
        session_update(ipInfos, email_send_last_time = time.time())
        session_update(ipInfos, email_send_count = ipInfos[0].email_send_count+1)

        token_hashed = Token.crypt_hash(token, hash_len=Token.HASH_EMAIL_TOKEN_LEN)
        model_update(self, cipher_token=token_hashed)

        session.commit()

    def token_auth(self, token_input)->bool:
        from database import session_update, session_get, IpInfos, model_get
        from begin.globals import Token

        ##
        ipInfos = session_get(IpInfos, hashed_ip=self.hashed_ip)
        session_update(ipInfos, auth_attempts=ipInfos[0].auth_attempts+1)

        #
        token = model_get(self, "cipher_token")[0]
        print('email_token: ', token)

        return Token.crypt_hash_auth(token, token_input)

    def token_valid(self)->bool:
        import time

        if self.validity < time.time():
            return False

        return True
