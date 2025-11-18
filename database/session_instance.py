from .session import *
from .session_methods import *

from .methods import *

##
def delete_objects():
    import shutil

    ##
    folder = ObjectCore.PATH_STORAGE

    os.makedirs(folder, exist_ok=True)

    for i in os.listdir(folder):
        shutil.rmtree(folder)

##
Icon.init_instances()

delete_objects()

session_insert(UserCore, name='Lorax', email='abcd@gmail.com', password='admin')
session_insert(UserInfos, userName='Lorax', nickname='Lorax')
