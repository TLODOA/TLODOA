from database.session import Base
from begin.globals import Token

##
class UserInfos(Base):
    __tablename__ = "UserInfos"

    DEFAULT_iconProfileName = "Lorax"
    DEFAULT_description = "Description not provide"
    DEFAULT_nickname = "Nickname not provide"

    ##
    def __init__(self, **kwargs)->None:
        import time

        #
        model = type("model", (self.__class__, ), {})

        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])

        #
        self.time_arrival = time.time()
        self.time_viewed_last = 0
