from begin.globals import Router, Scheduler, Config, SocketIO, Status, Token
from begin.xtensions import *

from database import *

##
app = flask.Flask(__name__)
app.config.from_object(Config)

scheduler = Scheduler.init()

#
Router.register(app)
Scheduler.register(scheduler)

SocketIO.socketio.init_app(app)

## Developer settings
session_insert(IpInfos, ip='127.0.0.1')
session_insert(UserCore, name='Lorax', email='abcd@gmail.com', password='admin', status=Status.OFFLINE)

user = session_query(UserCore, hashed_name=Token.crypt_sha256('Lorax'))
user_get = model_get(user[0], "cipher_name", "cipher_email")

print(user)
print(user_get)

session_update(user, email="aroba@gmail.com")

user = session_query(UserCore, hashed_email=Token.crypt_sha256('aroba@gmail.com'))
user_get = model_get(user[0], "cipher_email", "cipher_name")

print(user)
print(user_get)

##
"""
if __name__ == "__main__":
    scheduler.start()
    SocketIO.socketio.run(app, debug=True, host='0.0.0.0', port='5001')
"""
