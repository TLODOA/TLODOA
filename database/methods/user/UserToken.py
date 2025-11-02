from database.session import Base

##
class UserToken(Base):
    __tablename__ = 'UserToken'

    VALIDITY = 60*60*24

    ##
    def __init__(self, **kwargs)->None:

        from database import Token
        import time

        ##
        model = type("model", (self.__class__, ), {})

        if not "token" in kwargs.keys():
            token = Token.user_generate()

        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])

        self.validity = time.time() + self.VALIDITY

    def token_auth(self, token_input:str)->bool:
        from database import model_get
        from begin.globals import Token

        ##
        token = model_get(self, "cipher_token")[0]

        return Token.crypt_phash_auth(token, token_input)
