from begin.globals import Router, Scheduler, Config, SocketIO, Token
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

##
if __name__ == "__main__":
    scheduler.start()
    SocketIO.socketio.run(app, debug=True, host='0.0.0.0', port='5000')

