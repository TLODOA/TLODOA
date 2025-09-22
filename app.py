from begin import *

from database import *
from routers import *

##
app = flask.Flask(__name__)
app.config.from_object(Config)

router_register(app, ROUTER_PATH)

socketio.init_app(app)


##
if __name__=="__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port='5000')
