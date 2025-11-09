from database.session import Base
from begin.globals import Token

import time

##
class UserInfos(Base):
    __tablename__ = "UserInfos"

    DEFAULT_iconProfileName = "icon_profile_0"
    DEFAULT_description = "Description not provide"
    DEFAULT_nickname = "Nickname not provide"

    DEFAULT_time_arrival = time.time()
    DEFAULT_time_viewed_last = time.time()

    ##
    def __init__(self, **kwargs)->None:
        model = type("model", (self.__class__, ), {})

        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])
