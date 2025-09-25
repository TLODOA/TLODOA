from .xtensions import *

##
SECRET_KEY_LEN = 26

ROUTER_PATH = "routers"
ROUTER_REGISTER_IGNORE = ["__pycache__", "routers_register.py", "__init__.py", "cookies.py"]

socketio = flask_socketio.SocketIO()
