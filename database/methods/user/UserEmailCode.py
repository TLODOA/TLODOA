from database.session import Base

##
class UserEmailCode(Base):
    __tablename__ = 'UserEmailCode'

    VALIDITY = 60*30

    #
    FIELD_UNDEFINED = 0
    FIELD_LOGIN = 1
    FIELD_SIGN = 2

    FIELD_ABLE = [ FIELD_UNDEFINED, FIELD_SIGN, FIELD_LOGIN]

    ##
    def __init__(self, **kwargs)->None:
        from begin.globals import Token

        import time

        ##
        model = type("model", (self.__class__, ), {})

        if "token" not in kwargs.keys():
            kwargs["token"] = Token.email_generate()

        if "field" not in kwargs.keys():
            kwargs["field"] = self.FIELD_UNDEFINED

        #
        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])

        self.validity = time.time() + self.VALIDITY

    ##
    def token_send(self)->None:
        from database import session_update, session_query, model_get, model_update, IpInfos
        from begin.globals import Email, SMTP, Token

        from email.message import EmailMessage
        import smtplib
        import time

        ##
        ipInfos = session_query(IpInfos, hashed_ip=self.hashed_ip)
        status = ipInfos[0].email_send_status

        print('status send: ', status)
        if status != Email.SEND_OK:
            return

        ##
        email = model_get(self, "cipher_email")[0]
        token = model_get(self, "token")[0]

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

        token_hashed = Token.crypt_phash(token, hash_len=Token.PHASH_EMAIL_TOKEN_LEN)
        model_update(self, token=token_hashed)

    def token_auth(self, token_input)->bool:
        from database import session_update, session_query, IpInfos, model_get
        from begin.globals import Token

        ##
        ipInfos = session_query(IpInfos, hashed_ip=self.hashed_ip)
        session_update(ipInfos, auth_attempts=ipInfos[0].auth_attempts+1)

        #
        token = model_get(self, "token")[0]

        return Token.crypt_phash_auth(token, token_input)

    def token_valid(self)->bool:
        import time

        if self.validity < time.time():
            return False

        return True
