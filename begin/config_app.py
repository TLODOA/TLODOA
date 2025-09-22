from .globals import *

import os

class Config:
    SECRET_KEY = os.urandom(SECRET_KEY_LEN)
