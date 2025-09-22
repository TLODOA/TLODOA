from sqlalchemy import Column, String
from .base import Base

##
USER_CPF_LEN = 12
USER_NAME_LEN = 100

USER_EMAIL_LEN = 240
USER_PHONE_LEN = 20

USER_PASSWORD_LEN = 50

USER_STATUS_LEN = 20

##
class User(Base):
    __tablename__ = 'User'

    cpf = Column(String(USER_CPF_LEN), primary_key=True)
    name = Column(String(USER_NAME_LEN))

    email = Column(String(USER_EMAIL_LEN))
    phone = Column(String(USER_PHONE_LEN))

    password = Column(String(USER_PASSWORD_LEN))

    status = Column(String(USER_STATUS_LEN))
