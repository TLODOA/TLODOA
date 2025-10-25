import os
import itsdangerous

##
class Config:
    SECRET_KEY_LEN = 26

    SECRET_KEY = os.urandom(SECRET_KEY_LEN)

serializer = itsdangerous.URLSafeSerializer(Config.SECRET_KEY)
