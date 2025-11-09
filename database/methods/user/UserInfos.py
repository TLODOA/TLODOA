from database.session import Base

##
class UserInfos(Base):
    __tablename__ = "UserInfos"

    DEFAULT_description = "Description not provide"
    DEFAULT_photoPath = "image/icons/profile/icon_profile_0.png"
    DEFAULT_nickname = "Nickname not provide"

    ##
    def __init__(self, **kwargs)->None:
        import time

        ##
        model = type("model", (self.__class__, ), {})

        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])
        
        self.time_arrival = time.time()
        self.time_viewd_last = time.time()
