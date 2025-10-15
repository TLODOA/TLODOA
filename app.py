from begin import *

from database import *

from routers import *
from schedulers import *

from apscheduler.schedulers.background import BackgroundScheduler

##
app = flask.Flask(__name__)
app.config.from_object(Config)

scheduler = BackgroundScheduler()

#
register_router(app)
register_jobs(scheduler)

SocketIO.socketio.init_app(app)

## Developer settings
session_insert(IpInfos, ip='127.0.0.1')
# session_insert(UserEmailCode, ip='127.0.0.1', email='abcd@gmail.com', token='1234')
session_insert(User, name='Lorax', email='abcd@gmail.com', password='admin', status=Status.OFFLINE)

##
if __name__ == "__main__":
    scheduler.start()
    SocketIO.socketio.run(app, debug=True, host='0.0.0.0', port='5000')
