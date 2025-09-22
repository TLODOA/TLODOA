from .base import Base

from .User import USER_CPF_LEN
from .Bid import BID_ID_LEN

from sqlalchemy import Column, String, Integer, ForeignKey

##
class User_Bid(Base):
    __tablename__ = 'User_Bid'

    user_cpf = Column(String(USER_CPF_LEN), ForeignKey('User.cpf'), primary_key=True)
    bid_id = Column(String(BID_ID_LEN), ForeignKey('Bid.id'), primary_key=True)

    connections = Column(Integer)
