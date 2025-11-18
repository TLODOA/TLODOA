from .session import *
from .session_methods import *

from .methods import *

##
def delete_objects():
    import shutil

    ##
    file_zip = ObjectCore.PATH_STORAGE

    if not os.path.exists(file_zip):
        return

    os.remove(file_zip)

##
Icon.init_instances()

delete_objects()

session_insert(UserCore, name='Lorax', email='abcd@gmail.com', password='admin')
session_insert(UserInfos, userName='Lorax', nickname='Lorax')
