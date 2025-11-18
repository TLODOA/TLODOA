from begin.globals import Token

from database.session import Base
from database.session_methods import session_insert

import os
import re

##
class Icon(Base):
    __tablename__ = "Icon"

    #
    TYPE_UNDEFINED = 0
    TYPE_PROFILE = 1
    TYPE_BID = 2

    ICONS_PATH = "./static/image/icons"
    ICONS_TYPE = {
        TYPE_PROFILE: f"{ICONS_PATH}/profile",
        TYPE_BID: f"{ICONS_PATH}/bid"
    }

    ##
    def register(path:str, icon_type:int)->None:
        files = os.listdir(path)

        for i in files:
            file_name = i
            file_path = f"{path}/{i}"

            if os.path.isdir(file_path):
                add_icons(file_path)
                continue

            if not re.match(".*\\.png", file_name):
                continue

            icon_name = file_name.split('.')[0]
            icon_path = file_path.split('/')[2:]
            icon_path = '/'.join(icon_path)

            print('file_path:', file_path.encode(), icon_path)
            session_insert(Icon, type=icon_type, name=icon_name, pathIcon=icon_path)

    def init_instances()->None:
        for i in Icon.ICONS_TYPE.keys():
            Icon.register(Icon.ICONS_TYPE[i], i)
