from database.session import Base

##
class ObjectCore(Base):
    __tablename__ = "ObjectCore"

    ID_CHARS = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ123456789"
    ID_LEN = 7

    PATH_STORAGE = "./database/objects"

    ##
    def __init__(self, **kwargs)->None:
        import time

        ##
        model = type("model", (self.__class__, ), {})
        for i in kwargs.keys():
            if not i in model.__dict__.keys():
                continue

            setattr(self, i, kwargs[i])

        self.time_changed = time.time()
