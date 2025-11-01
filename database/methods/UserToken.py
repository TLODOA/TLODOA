from database.session import Base

##
class UserToken(Base):
    __tablename__ = 'UserToken'

    VALIDITY = 60*60*24

    ##
    def __init__( self
                 ,token:str=None
                 )->None:

        from database import Token
        import time

        ##
        if token is None:
            token = Token.user_generate()

        self.token = token
        self.validity = time.time() + self.VALIDITY

    def token_auth(self, token_input:str)->bool:
        from database import model_get
        from begin.globals import Token

        ##
        token = model_get(self, "cipher_token")[0]

        return Token.crypt_phash_auth(token, token_input)
