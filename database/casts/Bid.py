from .base import Base

from .User import USER_NAME_LEN

from sqlalchemy import Column, String, Integer, ForeignKey

##
BID_ID_LEN = 20

BID_NAME_LEN = 150

##
class Bid(Base):
    __tablename__ = 'Bid'

    id = Column(String(BID_ID_LEN), primary_key=True)
    name_owner = Column(String(USER_NAME_LEN), ForeignKey('User.name'))

    name = Column(String(BID_NAME_LEN))
    rate = Column(Integer)
