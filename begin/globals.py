from .xtensions import *

##
SECRET_KEY_LEN = 26


##
TOKEN_EMAIL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'
TOKEN_EMAIL_LEN = 7

#
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

SMTP_SENDER = 'tlodoa.official@gmail.com'
SMTP_APP_PASSWORD = 'acqq phxs kykf disb'


##
ROUTER_PATH = "routers"
ROUTER_REGISTER_IGNORE = ["__pycache__", "routers_register.py", "__init__.py", "cookies.py"]

##
socketio = flask_socketio.SocketIO()
