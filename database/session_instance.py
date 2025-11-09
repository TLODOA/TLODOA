from .session import *
from .session_methods import *

from .methods import *

from begin.globals import Token

##
Icon.init_instances()

session_insert(UserCore, name='Lorax', email='abcd@gmail.com', password='admin')
session_insert(UserInfos, userName='Lorax', nickname='Lorax')
