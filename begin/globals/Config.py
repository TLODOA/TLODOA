import os

##
class Config:
    SECRET_KEY_LEN = 26

    SECRET_KEY = os.urandom(SECRET_KEY_LEN)
