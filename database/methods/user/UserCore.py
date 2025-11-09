from database.session import Base

##
class UserCore(Base):
    __tablename__ = 'UserCore'

    STATUS_OFFLINE = 0
    STATUS_ONLINE = 1

    DEFAULT_status = STATUS_OFFLINE

    ##
    def __init__(self, **kwargs)->None:

        from begin.globals import Token

        ##
        model = type("model", (self.__class__, ), {})

        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])

        self.password = Token.crypt_phash(kwargs["password"])

    def password_auth(self, password_input:str)->bool:
        from begin.globals import Token
        from database import model_get

        ##
        password = model_get(self, "password")[0]

        return Token.crypt_phash_auth(password, password_input)
