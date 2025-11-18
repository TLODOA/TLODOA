from database.session import Base

##
class ObjectCore(Base):
    __tablename__ = "ObjectCore"

    ID_CHARS = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ123456789"
    ID_LEN = 7

    PATH_STORAGE = "./database/objects.zip"

    OBJECT_PHYSIC_MAX_LEN = 1024 * 512
    OBJECT_PHYSIC_MAX = 10

    INTERVAL_CREATION = 60 * 2 # two minutes

    #
    STATUS_OK = 0
    STATUS_BLOCKED_BECAUSE_INTERVAL = 1
    STATUS_BLOCKED_BECAUSE_AMOUNT = 2

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
