from database.session import Base

##
class UserCore(Base):
    __tablename__ = 'UserCore'

    ##
    def password_auth(self, password_input:str)->bool:
        from begin.globals import Token
        from database.session import model_get

        ##
        password = model_get(self, "cipher_password")[0]
        print('password_hashed: ', password)

        return Token.crypt_phash_auth(password, password_input)
